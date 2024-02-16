from django.db import models
from enum import Enum

class OrganisationType(Enum):
    DIRECT = 'direct'
    MSP = 'msp'
    MSP_ORG = 'msp_org'

class OrganisationStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class OrganisationAuthType(Enum):
    SSO = 'sso'
    LOGIN = 'login'

class Organisations(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[(tag.value, tag.name.title()) for tag in OrganisationType])
    is_client = models.BooleanField(default=False)
    domain_name = models.CharField(max_length=255)
    organisation_status = models.CharField(max_length=20, choices=[(tag.value, tag.name.title()) for tag in OrganisationStatus], default=OrganisationStatus.INACTIVE.value)
    short_name = models.CharField(max_length=255)
    dar_logo = models.CharField(max_length=255, default = '', null = True)
    light_logo = models.CharField(max_length=255, default = '', null = True)
    auth_type = models.CharField(max_length=20, choices=[(tag.value, tag.name.title()) for tag in OrganisationAuthType], default=OrganisationAuthType.LOGIN.value)
    parent_msp_id = models.BigIntegerField(null = True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
