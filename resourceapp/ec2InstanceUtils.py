import boto3
import requests

from botocore.exceptions import ClientError

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from .models import *

def get_instance_details(instanceId, region_name):
    try:
        ec2_client = boto3.client('ec2', 
                                  region_name=region_name,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                  )
        

        response = ec2_client.describe_instances(InstanceIds=[instanceId])

        instanceid = instanceId
        aws_region = region_name
        instance_type = ((response['Reservations'][0]['Instances'][0]['InstanceType']))
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        vpc_id = response['Reservations'][0]['Instances'][0]['VpcId']
        private_dns_name = response["Reservations"][0]["Instances"][0]["PrivateDnsName"]
        private_ip_address = response["Reservations"][0]["Instances"][0]["PrivateIpAddress"]
        public_dns_name = response["Reservations"][0]["Instances"][0]["PublicDnsName"]
        public_ip_address = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
        instance_name = (response["Reservations"][0]["Instances"][0]["Tags"][0])['Value']


        checkVpcInstance = Vpc.objects.filter(vpc_id =vpc_id).exists()
        if not checkVpcInstance:
            response = ec2_client.describe_vpcs(VpcIds=[vpc_id])
            if 'Vpcs' in response and len(response['Vpcs']) > 0:
                vpc_details = response['Vpcs'][0]
                
                cidr_block = vpc_details.get('CidrBlock', '')

                vpcObjCreate = Vpc(
                    vpc_id = vpc_id,
                    cidr = cidr_block,
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                )

                with transaction.atomic():
                    vpcObjCreate.save()
            else:
                pass

        ec2_instance = Ec2(
                instance_id=instanceid,
                aws_region=aws_region,
                instance_type=instance_type,
                state=state,
                vpc_id=Vpc.objects.get(vpc_id = vpc_id),
                private_dns_name=private_dns_name,
                private_ip_address=private_ip_address,
                public_dns_name=public_dns_name,
                public_ip_address=public_ip_address,
                instance_name=instance_name
            )

        with transaction.atomic():
            ec2_instance.save()

        return
    

    except ClientError as e:
        print("Error:", e)
        return None
    

def ec2_association_elastic_ips(instance_id, elastic_ip, aws_region):
    ec2_client = boto3.client('ec2', 
                                  region_name=aws_region,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                  )
    
    try:
        response = ec2_client.describe_addresses(PublicIps=[elastic_ip])
        if 'Addresses' in response and len(response['Addresses']) > 0:
            address = response['Addresses'][0]
            reverse_dns = address.get('Association', {}).get('ReverseDns', '')
            if address.get('Domain', '') == 'vpc':
                ip_type = "Public Ip"
            else:
                ip_type = "Private Ip"

            private_ip = address.get('PrivateIpAddress', '')

            # checkElasticIpObj = (Elastic_Ips.objects.get(ip = elastic_ip)).exists()

            if (Elastic_Ips.objects.filter(ip = elastic_ip)).exists() == False:
                savingElasticIpObj = Elastic_Ips(
                    ec2_id = Ec2.objects.get(instance_id = instance_id),
                    ip = elastic_ip,
                    private_ip = private_ip,
                    reverse_dns = reverse_dns if reverse_dns else None,
                    elastic_ip_type = ip_type,
                    created_at = timezone.now(),
                )

                with transaction.atomic():
                    savingElasticIpObj.save()

                get_all_instances = requests.get('http://127.0.0.1:8002/api/get-all-instances/')

                return JsonResponse({
                    'reverse_dns': reverse_dns,
                    'type': ip_type,
                    'private_ip': private_ip
                })
            
            elif (Elastic_Ips.objects.filter(ip = elastic_ip)).exists() == True:
                elasticIpUpdate = (Elastic_Ips.objects.get(ip = elastic_ip))
                
                elasticIpUpdate.private_ip = private_ip
                elasticIpUpdate.reverse_dns = reverse_dns if reverse_dns else None,
                elasticIpUpdate.elastic_ip_type = ip_type
                elasticIpUpdate.ec2_id = Ec2.objects.get(instance_id = instance_id)
                elasticIpUpdate.updated_at = timezone.now()
                elasticIpUpdate.save()
        else:
            return JsonResponse({'error': 'Elastic IP address not found.'})
    except Exception as e:
        return JsonResponse({'error': f'Failed to fetch Elastic IP details: {str(e)}'})
