from django.urls import path
from .views import *

urlpatterns = [
    path('api/create-instance/', create_ec2_instance, name='create_instance'),
    path('api/create-elastic-ip-and-allocate-ec2/',create_elastic_ip_and_allocate_ec2),
    path('api/get-all-instances/',get_all_instances)
]
