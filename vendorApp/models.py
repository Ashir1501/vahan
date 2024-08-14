from django.db import models
from usersApp.models import Account
# Create your models here.

class CarType(models.Model):
    car_model = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    car_brand = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_type}-{self.car_brand} {self.car_model}"
    
class Route(models.Model):

    TRIP_CHOICES = [
        ('oneway','oneway'),
        ('roundtrip','roundtrip'),
        ('local','local'),
        ('airport_pickup','airport_pickup'),
        ('airport_drop','airport_drop'),
    ]

    DURATION_CHOICES = (
        ('none','none'),
        ('4 hrs 40 km', '4 hrs 40 km'),
        ('8 hrs 80 km', '8 hrs 80 km'),
        ('12 hrs 120 km', '12 hrs 120 km')
    )
    trip_type = models.CharField(max_length=20,choices=TRIP_CHOICES)
    pickup_location = models.CharField(max_length=150)
    drop_location = models.CharField(max_length=150, null=True, blank=True)
    car_type = models.ManyToManyField(CarType)
    fare = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True, default=30)
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES, default=DURATION_CHOICES[0])
    kms = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.pickup_location}-{self.drop_location}-Car({self.car_type.get()})"




class Car(models.Model):
    Car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    Vender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    Front_pic = models.ImageField(upload_to='car_images', default=None)
    Back_pic = models.ImageField(upload_to='car_images', default=None)
    Registration_Number = models.CharField(max_length=20)
    rc_photo = models.ImageField(upload_to='car_images', default=None)
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.Car_type}-{self.Registration_Number}"

