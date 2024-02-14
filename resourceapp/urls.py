from django.urls import path
from .views import *

urlpatterns = [
    path('fetch-mysql-data-ec2/', fetchMySqlDataEc2),
    path('fetch-mysql-data-elastic-ips/', fetchMySqlDataElasticIps),
]