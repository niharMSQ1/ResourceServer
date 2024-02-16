from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import *

import boto3
import json

@csrf_exempt
def fetchAndSaveOrganisationsDetails(request):
    query = "SELECT * FROM organizations"
    data = fetch_data_from_mysql(query)

    for item in data:
        organisationInstance = Organisations(
            name = item[1],
            type= item[2],
            is_client= True if item[3] == 'yes' else False,
            domain_name= item[4],
            organisation_status= item[5],
            short_name= item[6],
            dar_logo= item[7],
            light_logo= item[8] if item[8] else None,
            auth_type= item[9],
            parent_msp_id= item[10],
            create_at= item[11],
            updated_at= item[12],

        )
        organisationInstance.save()

    return JsonResponse({
        
    })

@csrf_exempt
def copyingEc2FromSq1Cloud(request):
    query = "SELECT * FROM ec2"
    data = fetch_data_from_mysql(query)

    for item in data:
        ec2Instance = Ec2(
            org_id = Organisations.objects.get(pk = item[1]),
            vpc_id= item[2],
            name= True if item[3] == 'yes' else False,
            instance_id= item[4],
            instance_type= item[5],
            os= item[6],
            instance_status= item[7],
            public_dns= item[8] if item[8] else None,
            public_ip= item[9],
            private_ip= item[10],
            agent_status = item[11],
            created_at= item[12],
            updated_at= item[13],

        )
        ec2Instance.save()

    return JsonResponse({

    })

@csrf_exempt
def copyingElasticIpsFromSq1Cloud(request):
    query = "SELECT * FROM elastic_ips"
    data = fetch_data_from_mysql(query)

    for item in data:
        ElastipIpsInstance = ElastipIps(
            org_id = Organisations.objects.get(pk = item[1]),
            ec2_id = Ec2.objects.get(pk = item[2]),
            ip = item[3],
            private_ip = item[4],
            reverse_dns = item[5],
            type = item[6],
            created_at= item[7],
            updated_at= item[8],
        )
        ElastipIpsInstance.save()

    return JsonResponse({

    })

@csrf_exempt
def savingEc2ElasticIpsRelation(request):
    orgId = (json.loads(request.body)).get('orgId')

    CheckElasticIpsIdObj = (ElastipIps.objects.filter(org_id_id = orgId)).exists()

    if CheckElasticIpsIdObj:
        elastic_ips_objs = list(ElastipIps.objects.filter(org_id_id = orgId))

        ip_addresses = {}

        for elastic_ip_obj in elastic_ips_objs:
            ip = elastic_ip_obj.ip
            ec2_id = elastic_ip_obj.ec2_id_id
            ip_addresses[ec2_id] = ip


        print()