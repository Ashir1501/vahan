# Generated by Django 4.2.14 on 2024-09-27 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='OTP',
        ),
    ]
