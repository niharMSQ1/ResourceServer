# Generated by Django 5.0.2 on 2024-02-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisations',
            name='dar_logo',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='organisations',
            name='light_logo',
            field=models.CharField(default=None, max_length=255),
        ),
    ]