from django.db import models

from enum import Enum

class Organisation_type(Enum):
    MSP = 'msp'
    DIRECT = 'direct'
    MSP_ORF = 'msp_org'

class Client_Choices(Enum):
    YES = 'yes'
    NO = 'no'

class Organisation_status(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class Organisation_auth_type(Enum):
    SSO = 'sso'
    LOGIN = 'login'
class Organisation(models.Model):
    organization_id = models.CharField(max_length=255, null = True)
    organisation_type =  models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Organisation_type], default=Organisation_type.DIRECT.value)
    is_client =models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Client_Choices], default=Client_Choices.NO.value)
    domain_name = models.CharField(max_length=255, null = True)
    status = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Organisation_status], default=Organisation_status.INACTIVE.value)
    short_name = models.CharField(max_length=255, null = True)
    dark_logo = models.CharField(max_length=255, null = True)
    light_logo = models.CharField(max_length=255, null = True)
    auth_type = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Organisation_auth_type], default=Organisation_auth_type.LOGIN.value)
    parent_msp_id = models.BigIntegerField(null = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Vpc(models.Model):
    name = models.CharField(max_length=255, null = True)
    vpc_id = models.CharField(max_length=100)
    cidr =  models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

class Ec2(models.Model):
    instance_type = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    organisation_id = models.ForeignKey(Organisation, on_delete = models.CASCADE)
    vpc_id = models.ForeignKey(Vpc, on_delete = models.CASCADE)
    private_dns_name = models.CharField(max_length=255)
    private_ip_address = models.CharField(max_length=50)
    public_dns_name = models.CharField(max_length=255)
    public_ip_address = models.CharField(max_length=50)
    instance_name = models.CharField(max_length=255)
    instance_id = models.CharField(max_length=100)
    aws_region = models.CharField(max_length=100)

    def __str__(self):
        return self.instance_id
    
class Elastic_ip_type(Enum):
    PUBLIC_IP = "Public IP"
    PRIVATE_IP = "Private IP"
class Elastic_Ips(models.Model):
    ec2_id = models.ForeignKey(Ec2, on_delete = models.CASCADE)
    ip = models.CharField(max_length=45)
    private_ip = models.CharField(max_length=45)
    reverse_dns = models.CharField(max_length=255, null=True)
    organisation_id = models.ForeignKey(Organisation, on_delete = models.CASCADE)
    elastic_ip_type =  models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Elastic_ip_type], default=Elastic_ip_type.PUBLIC_IP.value)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


