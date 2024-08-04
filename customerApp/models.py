from django.db import models
from vendorApp.models import Route, Driver, Car
from usersApp.models import Account
# Create your models here.

class Ride(models.Model):
    
    RIDE_STATUS_CHOICES = (
        ('cancelled','cancelled'),
        ('Started','Started'),
        ('completed','completed')
    )

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    pickup_at = models.TimeField()
    return_date = models.DateField(null=True,blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    ride_status = models.CharField(max_length=20, choices=RIDE_STATUS_CHOICES)
    Front_pic = models.ImageField(upload_to='ride_images', default=None)
    Back_pic = models.ImageField(upload_to='ride_images', default=None)
    selfie = models.ImageField(upload_to='ride_images', default=None)
    opening_kms_screen = models.ImageField(upload_to='ride_images', default=None)
    closing_kms_screen = models.ImageField(upload_to='ride_images', default=None)

    def __str__(self):
        return f"{self.customer.name}-{self.route}-{self.pickup_date}"

class Extra(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    new_destination = models.CharField(max_length=100, default="none")
    kms = models.IntegerField()
    duration = models.DurationField()
    toll_fare = models.IntegerField(null=True,blank=True)
    parking_fare = models.IntegerField(null=True,blank=True)

    @property
    def extra_fare(self):
        return (self.kms*13.5)+self.toll_fare+self.parking_fare
    
    def __str__(self):
        return f"extra-{self.ride}"
    
