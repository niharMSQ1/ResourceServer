from django.urls import path
from .views import *

urlpatterns = [
    path('fetch-mysql-data/', fetchMySqlData)
]