from django.shortcuts import render, redirect, get_object_or_404
import hashlib
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages
from .models import *
from customerApp.models import *
from vendorApp.models import *
import uuid
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import json
import hmac
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.

def hash_id(objects):
    for obj in objects:
        obj.hashed_id = hashlib.sha256(str(obj.id).encode()).hexdigest()
    return objects

def decode_hashed_id(hashed_id, model_class):
    # Iterate over all objects and find the one with the matching hashed ID
    for obj in model_class.objects.all():
        generated_hash = hashlib.sha256(str(obj.id).encode()).hexdigest()
        print(f"Checking ID: {obj.id} -> Generated hash: {generated_hash}")
        if generated_hash == hashed_id:
            print(f"Match found for hashed ID: {hashed_id}")
            return obj.id
    print(f"No match found for hashed ID: {hashed_id}")
    return None


def email_temp(ride,payment,payment_method,razorpay_payment_id=None):
    subject = 'Payment recipt'
    print("line 47 :",ride)
    # customer email=========
    html_contentC = render_to_string('driverTemplates/payment_success_email.html', {
        'customer_first_name': ride.customer.first_name,
        'customer_last_name': ride.customer.last_name,
        'payment_id': razorpay_payment_id,
        'total_fare':payment.total_fare,
        'toll_fare':ride.toll_fare,
        'parking_fare':ride.parking_fare,
        'ride_fare':payment.pending_payment,
        'driver_name':ride.driver.first_name,
        'car_model':ride.car.Car_type.car_model,
        'car_type':ride.car.Car_type.car_type,
        'pick_up':ride.route.pickup_location,
        'drop':ride.route.drop_location,
        'payment_type':payment_method,
    })
    text_contentC = strip_tags(html_contentC)  
    
    emailC = EmailMultiAlternatives(subject, text_contentC, settings.DEFAULT_FROM_EMAIL, ['fcgaavez@gmail.com'])  # Replace with actual customer email
    emailC.attach_alternative(html_contentC, "text/html")
    emailC.send()
    # vendor email ===================
    html_contentV = render_to_string('driverTemplates/payment_success_email.html', {
        'customer_first_name': ride.customer.first_name,
        'customer_last_name': ride.customer.last_name,
        'payment_id': razorpay_payment_id,
        'total_fare':payment.total_fare,
        'toll_fare':ride.toll_fare,
        'parking_fare':ride.parking_fare,
        'vendor_name' : True,
        'ride_fare':payment.pending_payment,
        'driver_name':ride.driver.first_name,
        'car_model':ride.car.Car_type.car_model,
        'car_type':ride.car.Car_type.car_type,
        'pick_up':ride.route.pickup_location,
        'drop':ride.route.drop_location,
        'payment_type':payment_method,
    })
    text_contentV = strip_tags(html_contentV)  
    
    emailV = EmailMultiAlternatives(subject, text_contentV, settings.DEFAULT_FROM_EMAIL, ['aavezsid@gmail.com'])  # Replace with actual customer email
    emailV.attach_alternative(html_contentV, "text/html")
    emailV.send()

    # admin email==================
    html_contentA = render_to_string('driverTemplates/payment_success_email.html', {
        'customer_first_name': ride.customer.first_name,
        'customer_last_name': ride.customer.last_name,
        'payment_id': razorpay_payment_id,
        'total_fare':payment.total_fare,
        'toll_fare':ride.toll_fare,
        'parking_fare':ride.parking_fare,
        'admin' : True,
        'ride_fare':payment.pending_payment,
        'driver_name':ride.driver.first_name,
        'car_model':ride.car.Car_type.car_model,
        'car_type':ride.car.Car_type.car_type,
        'pick_up':ride.route.pickup_location,
        'drop':ride.route.drop_location,
        'payment_type':payment_method,
    })
    text_contentA = strip_tags(html_contentV)  
    
    emailA = EmailMultiAlternatives(subject, text_contentA, settings.DEFAULT_FROM_EMAIL, ['sidaavez@gmail.com'])  # Replace with actual customer email
    emailA.attach_alternative(html_contentA, "text/html")
    emailA.send()

def payment_callback(request):
    if request.method == "GET":
        # Extract parameters from the callback request
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        ride_id = request.GET.get('ride_id')
        razorpay_payment_link_status = request.GET.get('razorpay_payment_link_status')
        razorpay_signature = request.GET.get('razorpay_signature')
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        
        # Decode the ride ID
        ride = decode_hashed_id(ride_id, Ride)
        ride = get_object_or_404(Ride, id=ride)
        driver = ride.driver  # Assuming `driver` is a field in the `Ride` model
        
        # Retrieve or create payment record
        payment, created = Payment.objects.get_or_create(ride=ride)
        try:
            payment_details = client.payment.fetch(razorpay_payment_id)
            payment_method = payment_details.get('method', 'unknown')  # Get the payment method (upi, card, etc.)
        except razorpay.errors.BadRequestError as e:
            payment_method = 'unknown'
            
        if payment_method == 'upi':
            
            payment.pending_paymeny_Type = 'upi'
            
        elif payment_method == 'card':
            payment.pending_paymeny_Type = 'card'
            
        elif payment_method == 'netbanking':
            payment.pending_paymeny_Type = 'netbanking'
            
        elif payment_method == 'wallet':
            payment.pending_paymeny_Type = 'wallet'
            
 
        if razorpay_payment_link_status == 'success':
            payment.pending_payment_status = 'Success'
            message = "Payment success"
            payment.pending_razorpay_payment_id = razorpay_payment_id
        elif razorpay_payment_link_status == 'failed':
            payment.pending_payment_status = 'Failed'
            message = "Payment failed"
            payment.pending_razorpay_payment_id = razorpay_payment_id
        elif razorpay_payment_link_status == 'paid':
            payment.pending_payment_status = 'paid'
            message = "Payment done"
            payment.pending_razorpay_payment_id = razorpay_payment_id
        else:
            payment.pending_payment_status = 'pending'
            message = "Payment pending"
            payment.pending_razorpay_payment_id = razorpay_payment_id
        
        payment.save()
        print("line 174  :",f'driver_{driver.id}_group',)
        # Send notification to the specific driver's channel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'driver_{driver.id}_group',  # Unique group for the specific driver
            {
                'type': 'send_notification',
                'message': message
            }
        )
        if razorpay_payment_link_status == 'paid':
            email_temp(ride,payment,payment_method,razorpay_payment_id)
            return render(request, 'driverTemplates/payment_done.html')
        else:
            unique_reference_id = f"{ride_id}-{uuid.uuid4()}"
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment_link = client.payment_link.create({
                "amount": (int(payment.total_fare)) * 100,
                "currency": "INR",
                "accept_partial": False,
                "reference_id": unique_reference_id,
                "description": "Payment for your ride with Vaahan",
                "customer": {
                    "name": "Customer Name",
                    "email": "fcgaavez@gmail.com",
                    "contact": "9372004279"
                },
                "notify": {"sms": True, "email": True},
                "reminder_enable": True,
                "callback_url": f"http://127.0.0.1:8000/payment/callback/?ride_id={ride_id}&reference_id={unique_reference_id}",
                "callback_method": "get"
            })
            async_to_sync(channel_layer.group_send)(
            f'driver_{ride.id}_group',  # Unique group for the specific driver
            {
                'type': 'send_notification',
                'message': "Payment link shared again"
            }
            )
            payment.pending_paymeny_Type = 'online'
            return render(request, 'driverTemplates/payment_failed.html')

    return JsonResponse(request, 'Invalid request')

def ride_payment(request, hashed_id):
    # Decode ride ID from the hashed_id
    ride_id = decode_hashed_id(hashed_id, Ride)
    ride = get_object_or_404(Ride, id=ride_id)
    # payment = Payment.objects.filter(ride=ride).first()
    payment, created = Payment.objects.get_or_create(ride=ride)
    if request.method == 'POST':
        # Extract and process form data
        end_kms = request.POST.get('endKmsInput') or '0'
        end_kms_image_data = request.POST.get('end_kms_data')
        toll_fare = request.POST.get('tollFare') or '0'
        parking_fare = request.POST.get('parkingFare') or '0'
        pending_fare = request.POST.get('pendingFare') or '0'
        
        paymentType = request.POST.get('paymentDetail')
        # Process the image if provided
        end_kms_image_file = None
        if end_kms_image_data:
            format, imgstr = end_kms_image_data.split(';base64,')
            ext = format.split('/')[-1]
            end_kms_image_file = ContentFile(base64.b64decode(imgstr), name=f'end_kms_{ride_id}.{ext}')
        
        # Fare calculations
        try:
            end_kms = int(end_kms)
        except ValueError:
            end_kms = 0

        extra_fare = calculate_extra_fare(ride, end_kms)
        fare = Decimal(ride.fare) + extra_fare if ride.fare else extra_fare
        total_fare = Decimal(toll_fare) + Decimal(parking_fare) + fare

        if payment :
            if fare > Decimal(payment.advance_payment or 0) + Decimal(pending_fare):
                messages.error(request, "This ride has exceeded the kilometers it was booked for.")
                return redirect('driver-ongoing')
        print("line 122 :",f'driver_{ride.driver.id}_group')
        if paymentType=='online':
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'driver_{ride.driver.id}_group',  # Unique group for the specific driver
                {
                    'type': 'send_notification',
                    'message': "Payment link is Sharing"
                }
            )
            # Razorpay Payment Link Creation
            try:
                unique_reference_id = f"{ride_id}-{uuid.uuid4()}"
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment_link = client.payment_link.create({
                    "amount": (int(pending_fare) + int(toll_fare) + int(parking_fare)) * 100,
                    "currency": "INR",
                    "accept_partial": False,
                    "reference_id": unique_reference_id,
                    "description": "Payment for your ride with Vaahan",
                    "customer": {
                        "name": "Customer Name",
                        "email": "fcgaavez@gmail.com",
                        "contact": "9372004279"
                    },
                    "notify": {"sms": True, "email": True},
                    "reminder_enable": True,
                    "callback_url": f"http://127.0.0.1:8000/payment/callback/?ride_id={hashed_id}&reference_id={unique_reference_id}",
                    "callback_method": "get"
                })
                async_to_sync(channel_layer.group_send)(
                f'driver_{ride.id}_group',  # Unique group for the specific driver
                {
                    'type': 'send_notification',
                    'message': "Payment link shared"
                }
                )
                payment.pending_paymeny_Type = 'online'
            except:
                messages.error(request, "Razor Pay Error,please try again.")
                return redirect('driver-ongoing')
        
        else:
            
            payment.pending_payment_status = 'paid'
            payment.pending_paymeny_Type = 'cash'
            email_temp(ride,payment,"Cash")
            
        # Update ride status

        ride.toll_fare = toll_fare
        ride.parking_fare = parking_fare
        ride.closing_kms_input = end_kms
        ride.closing_kms_screen = end_kms_image_file
        ride.ride_status = 'completed'
        ride.save()

        payment.pending_payment = pending_fare
        payment.total_fare = total_fare
        payment.save()
        # Notify driver of link creation

        

        messages.success(request, "Ride completed.")
        return redirect('driver-ongoing')

    return render(request, 'driverTemplates/driver_ongoing_details.html', {'ride': ride})

def calculate_extra_fare(ride, end_kms):
    extra_fare = Decimal('0')
    if ride.route.kms:
        if ride.route.kms < end_kms - int(ride.opening_kms_input):
            ride.is_extra = True
            extra_fare = Decimal((end_kms - int(ride.opening_kms_input) - ride.route.kms) * 18)
    return extra_fare


def Payment_page(request):
    payment_data = Payment.objects.all()
    return render(request,'adminTemplates/PaymentTemp.html',{'payments':payment_data})