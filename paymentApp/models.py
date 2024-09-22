from django.db import models
from customerApp.models import Ride
# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS_CHOICE = (
        ('pending','pending'),
        ('paid','paid'),
        ('failed','failed')
    )
    PAYMENT_PERCENT_CHOICE=(
        ("25","25"),
        ("50","50")
    )
    PAYMENT_TYPE_CHOICE=(
        ('Wallet','Wallet'),
        ('credit','credit'),
        ('debit','debit')
    )
    PENDING_PAYMENT_TYPE_CHOICE=(
        ('upi','upi'),
        ('cash','cash'),
        ('wallet','wallet'),
        ('card','card'),
        ('netbanking','netbanking'),
    )

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE,null=True, blank=True)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    advance_payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICE,null=True, blank=True)
    pending_payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICE,null=True, blank=True)
    advance_payment = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    pending_payment = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    advance_payment_percent = models.CharField(max_length=10, choices=PAYMENT_PERCENT_CHOICE,null=True, blank=True)
    advance_payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICE,null=True, blank=True)
    pending_paymeny_Type = models.CharField(max_length=20, choices=PENDING_PAYMENT_TYPE_CHOICE,null=True, blank=True)
    advance_payment_date = models.DateTimeField(null=True, blank=True)
    pending_payment_date = models.DateTimeField(null=True, blank=True)
    advance_razorpay_payment_id = models.CharField(null=True, blank=True)
    pending_razorpay_payment_id = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"payment-{self.ride}"
    