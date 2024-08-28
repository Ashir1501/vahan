from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, phone_number,user_type,email=None,OTP=None,password=None, first_name=None, last_name=None):
        

        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            OTP = OTP,
            user_type = user_type,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, phone_number, email=None, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email = self.normalize_email(email),
            phone_number = phone_number,
            OTP = None,
            user_type = "Admin",
            first_name=first_name,
            last_name = last_name,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self.db)

class Account(AbstractBaseUser, PermissionsMixin):

    #required fields
    first_name = models.CharField(max_length = 150, null=True, blank=True)
    last_name = models.CharField(max_length = 150, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length = 10, unique=True)
    OTP = models.PositiveIntegerField(null=True)

    vendor = 'Vendor'
    admin = "Admin"
    driver = "Driver"
    customer = "Customer"

    CHOICES = (
        (vendor,vendor),
        (admin,admin),
        (driver,driver),
        (customer,customer)
    )
    #non required fields
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, null=True)
    last_login = models.DateField(null=True)
    user_type = models.CharField(max_length=255, choices=CHOICES, default=CHOICES[3][0])
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

class AccountDetail(models.Model):
    GENDER_CHOICES = [
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other"),
    ]
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accountDetail')
    photo = models.ImageField(upload_to='user_images', null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    driving_licence = models.ImageField(upload_to='user_images', null=True, blank=True)
    aadhar_card = models.ImageField(upload_to='user_images', null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Account,null=True, on_delete=models.SET_NULL)
    works_for = models.ForeignKey(Account,null=True,blank=True, on_delete=models.SET_NULL, related_name='worksFor')

    def __str__(self):
        return f"{self.user_id.first_name}-{self.user_id.last_name}"