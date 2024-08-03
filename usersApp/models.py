from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from random import randint
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, name, phone_number, email,user_type,OTP_verification=None,password=None):
        if not email:
            raise ValueError("User Must Have an Email Address")
        

        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,
            OTP_verification = OTP_verification,
            user_type = user_type,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, phone_number, email, password=None, name=None):
        user = self.create_user(
            email = self.normalize_email(email),
            phone_number = phone_number,
            OTP_verification = None,
            user_type = "Admin",
            name=name,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self.db)

class Account(AbstractBaseUser):

    #required fields
    name = models.CharField(max_length = 150, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length = 10, unique=True)
    OTP_verification = models.PositiveIntegerField(null=True)

    vendor = 'Vendor'
    customer = "Customer"

    CHOICES = (
        (vendor,vendor),
        (customer,customer)
    )
    #non required fields
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, null=True)
    last_login = models.DateField(null=True)
    user_type = models.CharField(max_length=255, choices=CHOICES, default=customer)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['phone_number', 'OTP_verification']
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        if self.email:
            return self.email
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
