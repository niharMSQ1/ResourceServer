# Generated by Django 5.0.2 on 2024-02-16 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourceapp', '0009_awsconfigurationdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='VPC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vpc_id', models.CharField(max_length=255)),
                ('cidr', models.CharField(max_length=255)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resourceapp.organisations')),
            ],
        ),
    ]
