from django.urls import path
from .views import fetchAndSaveOrganisationsDetails

urlpatterns = [
    path('fetch-and-save-organisations-details/', fetchAndSaveOrganisationsDetails),
]