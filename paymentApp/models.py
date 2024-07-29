from django.db import models
from customerApp.models import Ride
# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS_CHOICE = (
        ('pending','pending'),
        ('paid','paid')
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
        ('online','online'),
        ('cash','cash'),
        ('wallet','wallet')
    )

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICE)
    advance_payment = models.DecimalField(max_digits=10,decimal_places=2)
    advance_payment_percent = models.CharField(max_length=10, choices=PAYMENT_PERCENT_CHOICE)
    advance_payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICE)
    pending_paymeny_Type = models.CharField(max_length=20, choices=PENDING_PAYMENT_TYPE_CHOICE)