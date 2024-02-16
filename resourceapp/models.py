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

class AWSConfigurationDetails(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    region_name =models.CharField(max_length=255)
    access_key = models.TextField()
    secret_key =  models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class VPC(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    vpc_id = models.CharField(max_length=255)
    cidr = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InstanceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'

class AgentStatus(Enum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
class Ec2(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    vpc_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    instance_id = models.CharField(max_length=255)
    instance_type = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    instance_status = models.CharField(max_length = 20, choices=[(tag.value, tag.name.title()) for tag in InstanceStatus], default=InstanceStatus.STOPPED.value)
    public_dns = models.CharField(max_length=255)
    public_ip = models.CharField(max_length=255)
    private_ip = models.CharField(max_length=255)
    agent_status = models.CharField(max_length = 20, choices=[(tag.value, tag.name.title()) for tag in AgentStatus], default=AgentStatus.DISCONNECTED.value)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class SecurityGroups(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    ec2_id = models.ForeignKey(Ec2, on_delete = models.CASCADE)
    vpc_id = models.ForeignKey(VPC, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    group_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class ElasticIpsType(Enum):
    PUBLIC_IP = 'Public IP'
    PRIVATE_IP = 'Private'

class ElastipIps(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    ec2_id = models.ForeignKey(Ec2, on_delete = models.CASCADE)
    ip = models.CharField(max_length=20)
    private_ip = models.CharField(max_length = 45)
    reverse_dns = models.CharField(max_length=255)
    type = models.CharField(max_length = 20, choices=[(tag.value, tag.name.title()) for tag in ElasticIpsType], default=None)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class ElasticIps_Ec2_Relation(models.Model):
    org_id = models.ForeignKey(Organisations, on_delete = models.CASCADE)
    ec2_id = models.ForeignKey(Ec2, on_delete = models.CASCADE)
    instance_id = models.CharField(max_length=255)
    ip = models.CharField(max_length=20)