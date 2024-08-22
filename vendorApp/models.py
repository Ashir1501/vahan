from django.db import models
from usersApp.models import Account
# Create your models here.
# class Driver(models.Model):
#     name = models.CharField(max_length=150)
#     vendor_id = models.ForeignKey(Account, on_delete=models.CASCADE)
#     phone = models.CharField(max_length = 10, unique=True)
#     licence = models.ImageField(upload_to='driver_images', default=None)
#     aadhar_card = models.ImageField(upload_to='driver_images', default=None)
#     join_date = models.DateField()
#     exit_date = models.DateField()
#     otp = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='acc')

#     def __str__(self):
#         return f"{self.name}-{self.vendor_id.name}"

class CarType(models.Model):
    # car_model = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    # car_brand = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_type}"
    
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
    pickup_location = models.CharField(max_length=1000)
    drop_location = models.CharField(max_length=1000, null=True, blank=True)
    car_type = models.ForeignKey(CarType ,on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True, default=30)
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES, default=DURATION_CHOICES[0])
    kms = models.IntegerField(default=1)
    created_by =  models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.pickup_location}-{self.drop_location}-Car({self.car_type})"




class Car(models.Model):
    Car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    Vender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=50)
    car_brand = models.CharField(max_length=50)
    Front_pic = models.ImageField(upload_to='car_images', default=None)
    Back_pic = models.ImageField(upload_to='car_images', default=None)
    Registration_Number = models.CharField(max_length=20)
    rc_photo = models.ImageField(upload_to='car_images', default=None)
    is_available = models.BooleanField()
    created_by =  models.ForeignKey(Account, on_delete=models.CASCADE,related_name="created_by")
    def __str__(self):
        return f"{self.Car_type}-{self.Registration_Number}"

