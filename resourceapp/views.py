from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

from botocore.exceptions import ClientError

import json
import boto3
import threading
import time

from .ec2InstanceUtils import get_instance_details, ec2_association_elastic_ips
from .models import *


@csrf_exempt
def create_ec2_instance(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        instance_name = data.get('instance_name')
        checkInstanceObj = (Ec2.objects.filter(instance_name = instance_name)).exists()
        if checkInstanceObj == True:
            return JsonResponse({'success': False, 'error_message': "Instance name already exists, please choose a different Instance name"})

        instance_type = data.get('instance_type')
        image_id = data.get('image_id')
        aws_region = data.get('aws_region')

        try:
            ec2_client = boto3.client(
                'ec2',
                region_name=aws_region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            response = ec2_client.run_instances(
                ImageId=image_id,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': instance_name
                            },
                        ]
                    },
                ]
            )

            instance_id = response['Instances'][0]['InstanceId']

            def run_background_task():
                time.sleep(20)  # Waiting for 1 minute
                savingOnDb = get_instance_details(instance_id, aws_region)

            background_thread = threading.Thread(target=run_background_task)
            background_thread.start()

            return JsonResponse({'success': True, 'instance_id': instance_id})
    
        except ClientError as e:
            error_message = f"An error occurred: {e.response['Error']['Message']}"
            return JsonResponse({'success': False, 'error_message': error_message})

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

@csrf_exempt
def create_elastic_ip_and_allocate_ec2(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instance_id = data.get('instance_id')
        aws_region = data.get('aws_region')


        first_object_with_null_ec2_id = Elastic_Ips.objects.filter(ec2_id__isnull=True).first()
        if first_object_with_null_ec2_id:
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=aws_region
                )
            elastic_ip = first_object_with_null_ec2_id.ip
            ec2_client = session.client('ec2')

            response = ec2_client.describe_addresses()

            allocation_id = (response['Addresses'])[0]['AllocationId']
            try:
                ec2_client.associate_address(InstanceId=instance_id, AllocationId=allocation_id)

                def run_background_task():
                    time.sleep(30)  # Waiting for 30 seconds
                    savingOnDb = ec2_association_elastic_ips(instance_id, elastic_ip, aws_region)

                background_thread = threading.Thread(target=run_background_task)
                background_thread.start()

                return JsonResponse({'message': f'Elastic IP {elastic_ip} associated with instance {instance_id}'})
            except Exception as e:
                ec2_client.release_address(AllocationId=allocation_id)
                return JsonResponse({'error': f'Failed to associate Elastic IP with instance: {str(e)}'})


        else:
            ec2_client = boto3.client('ec2', region_name=aws_region,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            response = ec2_client.allocate_address(Domain='vpc')
            allocation_id = response['AllocationId']
            elastic_ip = response['PublicIp']

            try:
                ec2_client.associate_address(InstanceId=instance_id, AllocationId=allocation_id)

                def run_background_task():
                    time.sleep(30)  # Waiting for 30 seconds
                    savingOnDb = ec2_association_elastic_ips(instance_id, elastic_ip, aws_region)

                background_thread = threading.Thread(target=run_background_task)
                background_thread.start()

                return JsonResponse({'message': f'Elastic IP {elastic_ip} associated with instance {instance_id}'})
            except Exception as e:
                ec2_client.release_address(AllocationId=allocation_id)
                return JsonResponse({'error': f'Failed to associate Elastic IP with instance: {str(e)}'})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
    

@csrf_exempt
def ec2_table_cron(request):
    if request.method == 'POST':
        print()
        

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
    
@csrf_exempt
def get_all_instances(request):
    session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
    )

    ec2_client = session.client('ec2')

    response = ec2_client.describe_addresses()

    elastic_ips = response['Addresses']

    if len(elastic_ips)==0:
        return JsonResponse({
            "status":"Success",
            "message": f"No Elastic Ip for the region - {session.region_name}"
        })

    for ip in elastic_ips:
        elastic_ipp = ip['PublicIp']
        allocation_id = ip['AllocationId']

        checkElasticIpObj = (Elastic_Ips.objects.filter(ip=elastic_ipp)).exists()

        if not checkElasticIpObj:
            savingElasticIpObj = Elastic_Ips(
                                ec2_id = None,
                                ip = ip['PublicIp'],
                                private_ip = None,
                                reverse_dns = None,
                                elastic_ip_type = None,
                                created_at = timezone.now(),
                                )

            with transaction.atomic():
                savingElasticIpObj.save()

            elasticIpObj = Elastic_Ips.objects.get(ip = ip['PublicIp'])

            elastcEc2RelaObjSave = Elastic_Ips_Ec2_Relation(
                elastic_ip = elasticIpObj,
                elastic_ip_str = elasticIpObj.ip,
                ec2_id = None,
                ec2_id_str =None ,
                ec2_status = None,
                elastic_ip_status = Elastic_Ip_Current_Association.NOT_ASSOICATED.value,
            )

            with transaction.atomic():
                elastcEc2RelaObjSave.save()


        elif checkElasticIpObj: # Here we need to add new object which will have elastic_ip id w.r.t ec2 Instance
            ec2_id = ip.get('InstanceId') if ip.get('InstanceId') else Elastic_Ip_Current_Association.NOT_ASSOICATED.value
            if ec2_id == Elastic_Ip_Current_Association.NOT_ASSOICATED.value:
                elastcEc2RelaObj = Elastic_Ips_Ec2_Relation.objects.get(elastic_ip_str=elastic_ipp)
                
                elastic_ip_str = elastic_ipp
                elastcEc2RelaObj.ec2_id = None
                elastcEc2RelaObj.ec2_id_str = None
                elastcEc2RelaObj.ec2_status = None
                elastcEc2RelaObj.elastic_ip_status = Elastic_Ip_Current_Association.NOT_ASSOICATED.value
                elastcEc2RelaObj.save() 

                elastic_ipss = Elastic_Ips.objects.get(ip =elastic_ipp )
                elastic_ipss.ec2_id = None
                elastic_ipss.updated_at = timezone.now()
                elastic_ipss.save()


            else:
                Ec2obj = Ec2.objects.get(instance_id=ip.get('InstanceId'))
                if not (Elastic_Ips_Ec2_Relation.objects.filter(ec2_id = Ec2obj)).exists():
                    saving_elastic_ips_ec2_relation = Elastic_Ips_Ec2_Relation(
                        elastic_ip = Elastic_Ips.objects.get(ip =elastic_ipp ),
                        elastic_ip_str = elastic_ipp, 
                        ec2_id = Ec2obj,
                        ec2_id_str = Ec2obj.instance_id,
                        ec2_status = Ec2obj.state,
                        elastic_ip_status = Elastic_Ip_Current_Association.ASSOCIATED.value
                    )
                    saving_elastic_ips_ec2_relation.save()

        

        

    return JsonResponse({

    })