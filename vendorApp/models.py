from django.db import models
from usersApp.models import Account
# Create your models here.
class Driver(models.Model):
    name = models.CharField(max_length=150)
    vendor_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    phone = models.CharField(max_length = 10, unique=True)
    licence = models.BinaryField()
    aadhar_card = models.BinaryField()
    join_date = models.DateField()
    exit_date = models.DateField()
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='acc')

class Route(models.Model):

    TRIP_CHOICES = [
        ('oneway','oneway'),
        ('roundtrip','roundtrip'),
        ('local','local'),
        ('airport_pickup','airport_pickup'),
        ('airport_drop','airport_drop'),
    ]

    trip_type = models.CharField(max_length=20,choices=TRIP_CHOICES)
    pickup_location = models.CharField(max_length=150)
    drop_location = models.CharField(max_length=150)
    Car_type = models.ForeignKey('CarType', on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10,decimal_places=2)
    Duration = models.DurationField()
    kms = models.IntegerField()


class CarType(models.Model):
    Car_model = models.CharField(50)
    Car_brand = models.CharField(50)

class Car(models.Model):
    Car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    Vender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    MFG_Year = models.DateField()
    Front_pic = models.BinaryField()
    Back_pic = models.BinaryField()
    Registration_Number = models.CharField(max_length=20)
    rc_photo = models.BinaryField()
    area = models.CharField(20)
    available = models.BooleanField()


