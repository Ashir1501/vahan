# Generated by Django 4.2.14 on 2024-08-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerApp', '0005_remove_extra_fare'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='new_destination',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
