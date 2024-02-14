from django.db import models

# Create your models here.
class EC2(models.Model):
    organization_id = models.IntegerField()
    vpc_id = models.IntegerField()
    name = models.CharField(max_length = 1000)
    instance_id = models.CharField(max_length = 1000, unique=True)
    instance_type = models.CharField(max_length = 1000)
    os = models.CharField(max_length = 1000)

    INSTANCE_STATUS_CHOICES = (
        ('running', 'Running'),
        ('stopped', 'Stopped'),
    )

    instance_status = models.CharField(max_length=20, choices=INSTANCE_STATUS_CHOICES)

    public_dns = models.CharField(max_length = 1000, unique=True)
    public_ip = models.CharField(max_length = 1000, unique=True)
    private_ip = models.CharField(max_length = 1000, unique=True)

    AGENT_STATUS_CHOICES = (
        ('disconnected', 'Disconnected'),
        ('connected', 'Connected'),
    )

    agent_status = models.CharField(max_length=20, choices=AGENT_STATUS_CHOICES)

    create_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

class ElasticIps(models.Model):
    organization_id = models.IntegerField()
    ec2_id = models.IntegerField()
    ip = models.CharField(max_length = 1000, unique=True)
    private_ip = models.CharField(max_length = 1000, unique=True)
    reverse_dns = models.CharField(max_length = 1000, unique=True)


    IP_CHOICES = (
        ('public_ip', 'Public IP'),
        ('private_ip', 'Private IP'),
    )

    ip_type = models.CharField(max_length=20, choices=IP_CHOICES)

    create_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)