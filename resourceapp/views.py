from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import fetch_data_from_mysql

import boto3

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

    return JsonResponse({})

