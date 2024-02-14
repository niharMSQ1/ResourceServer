from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

import json
import mysql.connector
import datetime

from .models import *

# Create your views here.
@csrf_exempt
def fetchMySqlDataEc2(request):
    # cnx = mysql.connector.connect(
    #     host=settings.HOST,
    #     user=settings.USER,
    #     password=settings.PASSWORD,
    #     database=settings.NAME
    # )

    cnx = mysql.connector.connect(
        host='192.168.6.13',
        user='sq1cloud',
        password='$q1Cloud@123',
        database='sq1cloud'
    )

    

    cursor = cnx.cursor()
    query = "SELECT * FROM ec2"
    cursor.execute(query)


    data = list(cursor.fetchall())

    newData = []
    for i in data:
        intoList = list(i)
        newData.append(intoList)

    for item in newData:

        ec2_instance = EC2(
            organization_id=item[1],
            vpc_id=item[2],
            name=item[3],
            instance_id=item[4],
            instance_type = item[5],
            os=item[6],
            instance_status=item[7],
            public_dns=item[8],
            public_ip=item[9],
            private_ip=item[10],
            agent_status=item[11],
            create_at = item[12],
            updated_at = item[13]
            )
        ec2_instance.save()

    cursor.close()
    cnx.close()

    return JsonResponse({
        
    })

@csrf_exempt
def fetchMySqlDataElasticIps(request):
    cnx = mysql.connector.connect(
        host='192.168.6.13',
        user='sq1cloud',
        password='$q1Cloud@123',
        database='sq1cloud'
    )

    

    cursor = cnx.cursor()
    query = "SELECT * FROM elastic_ips"
    cursor.execute(query)


    data = list(cursor.fetchall())

    newData = []
    for i in data:
        intoList = list(i)
        newData.append(intoList)

    for item in newData:

        elastic_ips_instances = ElasticIps(
            organization_id=item[1],
            ec2_id=item[2],
            ip=item[3],
            private_ip=item[4],
            reverse_dns = item[5],
            ip_type=item[6],
            create_at = item[7],
            updated_at = item[8]
            )
        elastic_ips_instances.save()

    cursor.close()
    cnx.close()

    return JsonResponse({
        
    })

