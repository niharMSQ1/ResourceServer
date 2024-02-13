# Generated by Django 5.0.2 on 2024-02-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EC2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_id', models.IntegerField()),
                ('vpc_id', models.IntegerField()),
                ('name', models.CharField(max_length=1000)),
                ('instance_id', models.CharField(max_length=1000, unique=True)),
                ('instance_type', models.CharField(max_length=1000, unique=True)),
                ('os', models.CharField(max_length=1000)),
                ('instance_status', models.CharField(choices=[('running', 'Running'), ('stopped', 'Stopped')], max_length=20)),
                ('public_dns', models.CharField(max_length=1000)),
                ('public_ip', models.CharField(max_length=1000)),
                ('private_ip', models.CharField(max_length=1000)),
                ('agent_status', models.CharField(choices=[('disconnected', 'Disconnected'), ('connected', 'Connected')], max_length=20)),
                ('create_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
        ),
    ]
