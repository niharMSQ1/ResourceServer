from django.db import models

import enum

class Vpc(models.Model):
    name = models.CharField(max_length=255, null = True)
    vpc_id = models.CharField(max_length=100)
    cidr =  models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    

class Ec2(models.Model):
    instance_type = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
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
    
class Elastic_Ips(models.Model):
    ec2_id = models.ForeignKey(Ec2, on_delete = models.CASCADE)
    ip = models.CharField(max_length=45)
    private_ip = models.CharField(max_length=45)
    reverse_dns = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length = 255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


