from django.db import models
from vendorApp.models import Route, Car
from usersApp.models import Account
from datetime import timedelta
# Create your models here.

class Ride(models.Model):
    
    RIDE_STATUS_CHOICES = (
        ('pending','pending'),
        ('approved','approved'),
        ('confirmed','confirmed'),
        ('assigned','assigned'),
        ('cancelled','cancelled'),
        ('Started','Started'),
        ('completed','completed')
    )

    driver = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='driver_rides',null=True, blank=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    pickup_at = models.TimeField()
    return_date = models.DateField(null=True,blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE) 
    car =  models.ForeignKey(Car, on_delete=models.CASCADE,null=True, blank=True) 
    fare = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True, default=30)
    ride_status = models.CharField(max_length=20, choices=RIDE_STATUS_CHOICES,default=RIDE_STATUS_CHOICES[0])
    Front_pic = models.ImageField(upload_to='ride_images', default=None,null=True, blank=True)
    Back_pic = models.ImageField(upload_to='ride_images', default=None,null=True, blank=True)
    selfie = models.ImageField(upload_to='ride_images', default=None,null=True, blank=True)
    opening_kms_screen = models.ImageField(upload_to='ride_images', default=None,null=True, blank=True)
    closing_kms_screen = models.ImageField(upload_to='ride_images', default=None,null=True, blank=True)
    opening_kms_input = models.IntegerField(null=True, blank=True)
    closing_kms_input = models.IntegerField(null=True, blank=True)
    toll_fare = models.IntegerField(null=True,blank=True)
    parking_fare = models.IntegerField(null=True,blank=True)
    is_extra = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.first_name}-{self.route}-{self.pickup_date}"

# class Extra(models.Model):

#     Extra_PAYMENT_TYPE_CHOICE=(
#         ('online','online'),
#         ('cash','cash'),
#         ('wallet','wallet')
#     )

#     ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
#     new_destination = models.CharField(max_length=100, default="none")
#     kms = models.IntegerField(default="none")
#     duration = models.DurationField(default="none")
#     toll_fare = models.IntegerField(null=True,blank=True)
#     parking_fare = models.IntegerField(null=True,blank=True)
#     ride_fare = models.IntegerField(null=True,blank=True)
#     payment_type = models.CharField(max_length=20, choices=Extra_PAYMENT_TYPE_CHOICE)

#     @property
#     def extra_fare(self):
#         return (self.kms*13.5)+self.toll_fare+self.parking_fare
#     def set_duration(self, hours=0, minutes=0):
#         self.duration = timedelta(hours=hours, minutes=minutes)
#     def __str__(self):
#         return f"extra-{self.ride}"