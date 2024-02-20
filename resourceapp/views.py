from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from botocore.exceptions import ClientError

import json
import boto3
import threading
import time

from .ec2InstanceUtils import get_instance_details, ec2_association_elastic_ips


@csrf_exempt
def create_ec2_instance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        instance_type = data.get('instance_type')
        image_id = data.get('image_id')
        instance_name = data.get('instance_name')
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
                time.sleep(60)  # Waiting for 1 minute
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