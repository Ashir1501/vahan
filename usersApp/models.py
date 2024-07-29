from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, name, phonenumber, email, OTP_verification,user_type,created_at,updated_at):
        # if not email:
        #     raise ValueError("User Must Have an Email Address")
        
        # if not username:
        #     raise ValueError("User must have an username")

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phonenumber = phonenumber,
            OTP_verification = OTP_verification,
            user_type = user_type,
            created_at = created_at,
            updated_at = updated_at
        )

        
        user.save(using=self.db)
        return user


    def create_superuser(self, name, phonenumber, email, OTP_verification,user_type,created_at,updated_at):
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            phonenumber = phonenumber,
            OTP_verification = OTP_verification,
            user_type = user_type,
            created_at = created_at,
            updated_at = updated_at
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self.db)

class Account(AbstractBaseUser):

    #required fields
    name = models.CharField(max_length = 150)
    # last_name = models.CharField(max_length = 150)
    # username = models.CharField(max_length = 100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length = 10, unique=True)
    OTP_verification = models.CharField(max_length = 10)

    vendor = 'Vendor'
    customer = "Customer"

    CHOICES = (
        (vendor,vendor),
        (customer,customer)
    )
    #non required fields
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    last_login = models.DateField(auto_now_add = True)
    user_type = models.CharField(max_length=255, choices=CHOICES, default=customer)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    objects = MyAccountManager()
    

    REQUIRED_FIELDS = ['phone_number', 'OTP_verification']

    def __str__(self):
        if self.email:
            return self.email
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
