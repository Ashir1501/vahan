# Generated by Django 4.2.14 on 2024-08-08 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_model', models.CharField(max_length=50)),
                ('car_type', models.CharField(max_length=50)),
                ('car_brand', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_type', models.CharField(choices=[('oneway', 'oneway'), ('roundtrip', 'roundtrip'), ('local', 'local'), ('airport_pickup', 'airport_pickup'), ('airport_drop', 'airport_drop')], max_length=20)),
                ('pickup_location', models.CharField(max_length=150)),
                ('drop_location', models.CharField(blank=True, max_length=150, null=True)),
                ('fare', models.DecimalField(blank=True, decimal_places=2, default=30, max_digits=10, null=True)),
                ('duration', models.CharField(choices=[('none', 'none'), ('4 hrs 40 km', '4 hrs 40 km'), ('8 hrs 80 km', '8 hrs 80 km'), ('12 hrs 120 km', '12 hrs 120 km')], default=('none', 'none'), max_length=50)),
                ('kms', models.IntegerField(default=1)),
                ('car_type', models.ManyToManyField(to='vendorApp.cartype')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Front_pic', models.ImageField(default=None, upload_to='car_images')),
                ('Back_pic', models.ImageField(default=None, upload_to='car_images')),
                ('Registration_Number', models.CharField(max_length=20)),
                ('rc_photo', models.ImageField(default=None, upload_to='car_images')),
                ('is_available', models.BooleanField()),
                ('Car_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendorApp.cartype')),
                ('Vender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
