from django.db import models
from vendorApp.models import Route, Driver, Car
from usersApp.models import Account
# Create your models here.
class Extra(models.Model):
    Route = models.ForeignKey(Route, on_delete=models.CASCADE)
    duration = models.DurationField()
    kms = models.IntegerField()
    Fare = models.DecimalField(max_digits=10,decimal_places=2)

class Ride(models.Model):
    
    RIDE_CHOICES = (
        ('cancelled','cancelled'),
        ('Started','Started'),
        ('completed','completed')
    )

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    costomer = models.ForeignKey(Account, on_delete=models.CASCADE)
    Car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    pickup_at = models.TimeField()
    return_date = models.DateField
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    ride_status = models.CharField(max_length=20, choices=RIDE_CHOICES)
    ride_fare = models.DecimalField(max_digits=10, decimal_places=2)
    timing = models.TimeField()
    Extra = models.ForeignKey(Extra, on_delete=models.SET_NULL, null=True)
    Front_pic = models.BinaryField()
    Back_pic = models.BinaryField()
    selfie = models.BinaryField()
