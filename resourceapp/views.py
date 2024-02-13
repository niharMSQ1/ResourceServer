from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import json
import mysql.connector
import datetime

from .models import EC2

# Create your views here.
@csrf_exempt
def fetchMySqlData(request):
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


    data = cursor.fetchall()

    for item in data:  # Exclude the first element
        ec2_instance = EC2(
            organization_id=item[0],
            vpc_id=item[1],
            name=item[3],
            instance_id=item[4],
            os=item[5],
            instance_status=item[6],
            public_dns=item[7],
            public_ip=item[8],
            create_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
    ec2_instance.save()

    cursor.close()
    cnx.close()

    return JsonResponse({
        
    })