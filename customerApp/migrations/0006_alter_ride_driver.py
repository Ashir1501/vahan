# Generated by Django 5.1 on 2024-08-11 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerApp', '0005_alter_ride_driver'),
        ('vendorApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendorApp.driver'),
        ),
    ]
