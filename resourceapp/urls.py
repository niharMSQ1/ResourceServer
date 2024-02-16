from django.urls import path
from .views import *

urlpatterns = [
    path('fetch-and-save-organisations-details/', fetchAndSaveOrganisationsDetails),
    path('copying-ec2-from-sq1cloud/', copyingEc2FromSq1Cloud),
    path('copying-elastic-ips-from-sq1Cloud/',copyingElasticIpsFromSq1Cloud),
    path('saving-Ec2-ElasticIps-Relation/',savingEc2ElasticIpsRelation)
]