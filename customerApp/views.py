from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from usersApp.models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
import hashlib
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from collections.abc import Iterable
from django.db.models import Q
from paymentApp.models import *
import uuid
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile
import base64
from django.template.loader import get_template, render_to_string
import pdfkit
# Create your views here.

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# ===============================================================Rides views============================================
            # --------------------Pending Rides Views-------------------------


def hash_id(objects):
    if isinstance(objects, Iterable) and not isinstance(objects, str):  # Check if it's an iterable (excluding strings)
        for obj in objects:
            obj.hashed_id = hashlib.sha256(str(obj.id).encode()).hexdigest()
    else:  # Handle single object
        objects.hashed_id = hashlib.sha256(str(objects.id).encode()).hexdigest()
    
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


# method to render pending rides page
@login_required(login_url='auth/login/')
def Pending_rides_page(request):
    print("3 5 :",request.user.user_type)
    rides_details = Ride.objects.all()
    drivers = Account.objects.all()
    cars_data = Car.objects.all()

    rides_details = hash_id(rides_details)
    drivers_details = hash_id(drivers)
    cars = hash_id(cars_data)
    return render(request,'adminTemplates/ride_details.html',{'ridesData':rides_details,"driverData":drivers_details,"cars_data":cars})



# def autocomplete_driver(request):
#     if request:
#         query = request.GET.get('term', '')
#         if query:
#             users = Driver.objects.filter(name__icontains=query) 
#         else:
#             users = Driver.objects.all()
#         print("19 :",users)
#         results = []
#         for user in users:
#             user_json = {
#                 'id': user.id,
#                 'label': f"{user.name}",
#                 'value': user.name,  # This will display in the input box
                
#             }
#             results.append(user_json)
#         print("29 :",results)
#         return JsonResponse(results, safe=False)
#     return JsonResponse({'error': 'Not an AJAX request'}, status=400)

# method to assign driver


@login_required(login_url='auth/login/')
def assign_driver(request):
    if request.method == 'POST':
        hashed_driver_id = request.POST.get('driver_id')
        hashed_ride_id = request.POST.get('ride_id')
        hashed_car_id = request.POST.get('car_id')
        
        print("68 :" ,hashed_driver_id,hashed_ride_id)
        if hashed_driver_id and hashed_ride_id and hashed_car_id:
            # Decode the hashed IDs
            ride_id = decode_hashed_id(hashed_ride_id, Ride)
            driver_id = decode_hashed_id(hashed_driver_id, Account)
            car_id = decode_hashed_id(hashed_car_id,Car)
            print(7555 , car_id,driver_id,ride_id)
            if ride_id and driver_id:
                try:
                    ride_instance = get_object_or_404(Ride, id=ride_id)
                    driver = get_object_or_404(Account, id=driver_id)
                    car = get_object_or_404(Car,id = car_id)
                    print("line  92")
                    if Ride.objects.filter(driver=driver, pickup_date=ride_instance.pickup_date).exclude(id=ride_instance.id).exists():
                        messages.error(request, f"The driver {driver} is already assigned to another ride on {ride_instance.pickup_date}.")
                        return redirect('vendor-rides')
                    if Ride.objects.filter(car=car, pickup_date=ride_instance.pickup_date).exclude(id=ride_instance.id).exists():
                        messages.error(request,f"The car {car} is already assigned to another ride on {ride_instance.pickup_date}.")
                        return redirect('vendor-rides')
                    ride_instance.driver = driver
                    ride_instance.car = car
                    
                    if ride_instance.ride_status == 'confirmed':
                        ride_instance.ride_status = 'assigned'
                    
                    ride_instance.save()
                    
                    messages.success(request, f"Ride Assigned to {driver.first_name} {driver.last_name} with Car {car.Car_type.car_model} {car.Car_type.car_brand}")
                    return redirect('vendor-rides')
                except Exception as e:
                    print("line 110 :",e)
                    messages.error(request, 'Invalid Driver or Ride Data')
                    return redirect('vendor-rides')
            else:
                messages.error(request, 'Invalid Driver or Ride Data')
                return redirect('vendor-rides')
        else:
            messages.error(request, "Invalid Data")
            return redirect('vendor-rides')
        
       
    
    return redirect('vendor-rides')

@login_required(login_url='auth/login/')
def approved_ride(request):
    if request.method == 'POST':
        try:
            hashed_ride_ids = request.POST.getlist('ride_ids[]') 
            ride_ids = [decode_hashed_id(hashed_id, Ride) for hashed_id in hashed_ride_ids]

            # Filter rides by the decoded IDs and update their status
            affected_rows = Ride.objects.filter(id__in=ride_ids).update(ride_status='approved')
            return JsonResponse({'success': True, 'deleted_count': 1})
        except:
            pass
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
# method to render ongoing page

def ongoing_rides_page(request):
    print("line 158 =:",request.user.user_type)
    if request.user:
       
        if request.user.user_type == "Admin":
            print("if Admin Condition")
            rides_details = Ride.objects.all()
            print(rides_details)
        elif request.user.user_type == 'Vendor':
            try:
                rides_details = Ride.objects.filter(vendor_id = request.user.id)
            except:
                rides_details = []
        elif request.user.user_type == 'Driver':
            try:
                rides_details = Ride.objects.filter(driver = request.user.id)
            except:
                rides_details = []
        else:
            raise Http404("Page Not Found")
        for ride_detail in rides_details:
            ride_detail.hashed_id = hashlib.sha256(str(ride_detail.id).encode()).hexdigest()
        
    else:
        raise Http404("Page Not Found")
    print("line 149 :",rides_details,request.user.id)
    return render(request,'adminTemplates/ongoing.html',{'ridesData':rides_details})

 # -------------------------Completed Ride ----------------------------
@login_required(login_url='auth/login/')
def completed_or_past_rides(request):
    today = date.today()

    # Filter rides based on user type
    if request.user.user_type == 'Admin':
        rides = Ride.objects.filter(
            Q(ride_status='completed') | Q(pickup_date__lt=today)
        )
    elif request.user.user_type == 'Vendor':
        rides = Ride.objects.filter(
            (Q(ride_status='completed') | Q(pickup_date__lt=today)) & Q(vendor_id=request.user.id)
        )
    elif request.user.user_type == 'Driver':
        rides = Ride.objects.filter(
            (Q(ride_status='completed') | Q(pickup_date__lt=today)) & Q(driver=request.user.id)
        )
    else:
        raise Http404("Page Not Found")

    # Attach payment details and hashed_id to each ride
    for ride in rides:
        try:
            
            ride.payment_detail = Payment.objects.get(ride=ride)
        except Payment.DoesNotExist:
            ride.payment_detail = None
        # ride.hashed_id = hashlib.sha256(str(ride.id).encode()).hexdigest()
    rides = hash_id(rides)
    # Debugging output
    for ride in rides:
        try:
            print(f"Ride ID: {ride.hashed_id}, Payment Detail: {ride.payment_detail.id}")
        except:
            pass
    
    
    return render(request, 'adminTemplates/previous.html', {'ridesData': rides})

# ---cancel Ride ------- 
@login_required(login_url='auth/login/')
def cancel_ride(request):
    if request.method == 'POST':
        try:
            hashed_ride_ids = request.POST.getlist('ride_ids[]') 
            ride_ids = [decode_hashed_id(hashed_id, Ride) for hashed_id in hashed_ride_ids]

            # Filter rides by the decoded IDs and update their status
            affected_rows = Ride.objects.filter(id__in=ride_ids).update(ride_status='cancelled')
            return JsonResponse({'success': True, 'deleted_count': 1})
        except:
            pass
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# ----------------------- extra page ---------------------------
@login_required(login_url='auth/login/')
def extra_page(request, hashed_id):
    # Find the Ride object that corresponds to the hashed_id
    rides = Ride.objects.all()
    ride = None
    for item in rides:
        if hashlib.sha256(str(item.id).encode()).hexdigest() == hashed_id:
            ride = item
            break

    if ride is None:
        return render(request, 'adminTemplates/extra_page.html', {'error': 'Ride not found'})

    # Fetch and hash all Extra objects related to this Ride
    extras = hash_id(Extra.objects.filter(ride=ride.id))

    # Hash the Ride object
    ride.hashed_id = hashlib.sha256(str(ride.id).encode()).hexdigest()
    current_date = make_aware(datetime.now()).date()

    # Convert ride dates to date objects if they are datetime
    if ride.pickup_date:
        pickup_date = ride.pickup_date.date() if isinstance(ride.pickup_date, datetime) else ride.pickup_date
    if ride.return_date:
        return_date = ride.return_date.date() if isinstance(ride.return_date, datetime) else ride.return_date

    # Determine if the button should be displayed
    show_button = True
    if ride.route.trip_type == 'roundtrip':
        print("180 if")
        if return_date and current_date >= return_date + timedelta(days=3):
            show_button = False
    else:
        print("Else 184")
        if pickup_date and current_date >= pickup_date + timedelta(days=3):
            show_button = False
    print("Extra Status :",return_date + timedelta(days=2))
    context = {
        'ride': ride,
        'extras': extras,  # This will be a list of Extra objects
        'show_button': show_button,
    }
    for extra in extras:
        print("196  :",extra.new_destination)
    return render(request, 'adminTemplates/extra_page.html', context)


           
@login_required(login_url='auth/login/')
def add_new_extra(request):
    if request.method == 'POST':
        # Fetch the Ride object using the hashed ID
        
        hashed_id = request.POST.get('ride_id')
        url = reverse('extra-page', args=[hashed_id])
        ride = None
        for item in Ride.objects.all():
            if hashlib.sha256(str(item.id).encode()).hexdigest() == hashed_id:
                ride = item
                break
        
        if not ride:
            return HttpResponse("Ride not found", status=404)
        
        # Collect form data
        new_destination = request.POST.get('new_destination')
        kms = request.POST.get('ExtraKms')
        duration_str = request.POST.get('extraDuration', '0:0').strip() 
        toll_fare = request.POST.get('TollFare', '0')
        parking_fare = request.POST.get('ParkingFare', '0')
        ride_fare = request.POST.get('Ride Fare')
        payment_type = request.POST.get('Payment')
        

        if not kms or not ride_fare:
            messages.error(request,'KMs and Ride Fare are mandatory fields.')
            return redirect(url)

        try:
            kms = int(kms)
            ride_fare = int(ride_fare)
            toll_fare = int(toll_fare) if toll_fare else 0  # Default to 0 if empty
            parking_fare = int(parking_fare) if parking_fare else 0
        except ValueError:
            messages.error(request,'KMs, Ride Toll and parking Fare must be valid numbers.')
            return redirect(url)
        

        # Parse the duration string (assuming the input is in the format "hours:minutes")
        try:
            # Parse the duration string (assuming the input is in the format "HH:MM")
            parts = duration_str.split(':')
            if len(parts) == 2:
                hours, minutes = map(int, parts)
                

            else:
                hours, minutes = 0, 0  # Default values if format is incorrect
            duration = timedelta(hours=hours, minutes=minutes)
            print(f"Parsed hours: {hours}, minutes: {minutes}")
            print(f"Duration: {duration}")
        except ValueError:

            messages.error(request,"Invalid duration format. Please use 'HH:MM'.", status=400)
            
            return redirect(url)

        # Create and save the new Extra object
        extra = Extra(
            ride=ride,
            new_destination=new_destination,
            kms=kms,
            toll_fare=toll_fare,
            parking_fare=parking_fare,
            ride_fare=ride_fare,
            payment_type=payment_type,
            duration=duration
        )
        extra.set_duration(hours=hours, minutes=minutes)
        extra.save()

        return redirect(url)  # Redirect to a success page or back to the form

    return HttpResponse("Invalid request", status=400)

@login_required(login_url='auth/vendor/login/')  
def delete_Extra(request):
    if request.method == 'POST':
        hashed_ids = request.POST.getlist('extra_ids[]')  # Get the list of car IDs
        print("Car IDs to delete:", hashed_ids)

        try:
            # Use filter to delete all cars with the provided IDs
            original_ids = [decode_hashed_id(hid, Extra) for hid in hashed_ids]
            original_ids = [id for id in original_ids if id is not None]  # Filter out None values
            
            if not original_ids:
                return JsonResponse({'success': False, 'error': 'No valid Extra found to delete'}, status=404)

            # Use filter to delete all Extras with the provided original IDs
            extras = Extra.objects.filter(id__in=original_ids)
            deleted_count, _ = extras.delete()  # Delete the cars and get the count of deleted items
            
            if deleted_count > 0:
                return JsonResponse({'success': True, 'deleted_count': deleted_count})
            else:
                return JsonResponse({'success': False, 'error': 'No Extra found to delete'}, status=404)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required(login_url='auth/vendor/login/') 
def vendor_ride_details(request):
    
    rides_details = Ride.objects.all()
    drivers = Account.objects.all()
    cars_data = Car.objects.all()
    rides_details = hash_id(rides_details)
    drivers_details = hash_id(drivers)
    cars = hash_id(cars_data)
    for ride in rides_details:
        ride.fare_20_percent = round(float(ride.fare) * 0.2, 2)
    return render(request, 'vendorTemplates/vendors_ride_details.html', {
        'ridesData': rides_details,
        'driverData': drivers_details,
        'cars_data': cars
    })

# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def confirmed_ride_status(request):
    if request.method == 'POST':
        ride_id_hashed = request.POST.get('ride_id')
        ride_id = decode_hashed_id(ride_id_hashed, Ride)
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        try:
            ride = Ride.objects.get(id=ride_id)
            ride.ride_status = 'confirmed'
            ride.vendor_id = Account.objects.get(id=request.user.id)
            ride.save()
            
            # Optionally verify payment signature with Razorpay server here
            # response = verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
            # if not response['status'] == 'success':
            #     return JsonResponse({'success': False, 'message': 'Payment verification failed'})
            
            return JsonResponse({'success': True, 'message': 'Ride status updated to confirmed'})
        except Ride.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ride not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def vendor_suggestions(request):
    # Fetch drivers data and hash their IDs
    drivers = Account.objects.all()
    driver_data = []  # Initialize list for driver data

    for driver in drivers:
        account_details = AccountDetail.objects.filter(user_id=driver.id, works_for=request.user.id)
        # Hash the account details
        hashed_details = hash_id(account_details)

        for detail in hashed_details:  # Ensure we are iterating over the hashed details
            driver_data.append({
                "name": f"{driver.first_name} | {driver.last_name} | {driver.email}",
                "hashed_id": detail.hashed_id,  # Use the hashed_id from the detail
            })

    # Fetch car data and hash their IDs
    cars = Car.objects.filter(Vender_id=request.user.id)
    car_data = []  # Initialize list for car data
    print(cars)
    hashed_cars = hash_id(cars)  # Hash the car objects
    for car in hashed_cars:  # Iterate over the hashed cars
        car_data.append({
            "name": f"{car.Car_type.car_model} | {car.Registration_Number} | {car.Car_type.car_type}",
            "hashed_id": car.hashed_id,  # Use the hashed_id from the car object
        })

    return JsonResponse({"drivers": driver_data, "cars": car_data}, safe=False)




# def driver_ride_details(request):
#     if request.user.user_type == 'Driver':
#         # # Filter rides by the current driver's ID and assigned status
#         # rides = Ride.objects.filter(
#         #     Q(driver=request.user.id) & Q(ride_status="assigned")
#         # )
#         # print("441  : ",request.user)
#         # ride_details = []
#         # # Assuming hash_id function correctly modifies the queryset
#         # rides = hash_id(rides)

#         # for ride in rides:
#         #     # Get the payment details for the ride
#         #     payment = Payment.objects.filter(ride=ride).first()  # Get the first payment entry

#         #     # Calculate remaining fare
#         #     if payment and payment.advance_payment is not None and ride.fare is not None:
#         #         remaining_fare = ride.fare - payment.advance_payment
#         #     else:
#         #         remaining_fare = ride.fare if ride.fare is not None else 0

#         #     # Add ride details and payment info
#         #     ride_details.append({
#         #         'ride': ride,
#         #         'advance_payment': payment.advance_payment if payment else None,
#         #         'remaining_fare': remaining_fare
#         #     })

#         # print("line 454:", ride_details)
#         # return render(request, 'driverTemplates/driver_ride_details.html', {'rides': ride_details})
#         return redirect('driver-home')
#     else:
#         raise Http404("Page Not Found")

def driver_ongoing_details(request):
    if request.user.user_type == 'Driver':
        rides = Ride.objects.filter(driver=request.user.id, ride_status="Started")
        
        # Hash the IDs of the rides
        rides = hash_id(rides)
        
        ride_details = []

        for ride in rides:
            # Fetch the related payment, if it exists
            payment = Payment.objects.filter(ride=ride).first()
            
            # Calculate remaining fare
            advance_payment = payment.advance_payment if payment else 0
            remaining_fare = ride.fare - (advance_payment or 0) if ride.fare else 0


            # Append ride details with additional information
            ride_details.append({
                'ride': ride,
                # 'ride_id_hashed': ride.hashed_id,  # Use the hashed ID
                'advance_payment': advance_payment,
                'remaining_fare': remaining_fare
            })
        print(ride_details)
        return render(request, 'driverTemplates/driver_ongoing_details.html', {'rides': ride_details})
    else:
        raise Http404("Page Not Found")

    

@csrf_exempt  # Use with caution; ensure you handle CSRF properly in production
def start_ride(request):
    if request.method == 'POST' and request.user.user_type == 'Driver':
        hashed_id = request.POST.get('ride_id')
        front_car_image = request.POST.get("front_car_image_data")
        back_car_image = request.POST.get("back_car_image_data")
        selfie_image_data = request.POST.get("selfie_image_data")
        kms_image_data = request.POST.get("kms_image_data")
        start_kms_input = request.POST.get("start_kms_input")
        print("line 448:", hashed_id)

        # Decode the hashed_id to get the original ride ID
        ride_id = decode_hashed_id(hashed_id, Ride)
        print("line 449:", ride_id)
        
        # Check if the driver already has any ride with the status "Started"
        existing_started_ride = Ride.objects.filter(driver=request.user.id, ride_status="Started").exists()
        print("501 ::", existing_started_ride)

        if existing_started_ride:
            return JsonResponse({'status': 'error', 'message': 'You already have a started ride. Complete it before starting a new one.'}, status=400)

        # Decode and save the car image
        front_car_image_file = None
        if front_car_image:
            format, imgstr = front_car_image.split(';base64,')
            ext = format.split('/')[-1]
            front_car_image_file = ContentFile(base64.b64decode(imgstr), name=f'car_{ride_id}.{ext}')
            print("Decoded car image:", front_car_image_file)

        back_car_image_file = None
        if back_car_image:
            format, imgstr = back_car_image.split(';base64,')
            ext = format.split('/')[-1]
            back_car_image_file = ContentFile(base64.b64decode(imgstr), name=f'car_{ride_id}.{ext}')
            print("Decoded car image:", back_car_image_file)

        # Decode and save the selfie image
        selfie_image_file = None
        if selfie_image_data:
            format, imgstr = selfie_image_data.split(';base64,')
            ext = format.split('/')[-1]
            selfie_image_file = ContentFile(base64.b64decode(imgstr), name=f'selfie_{ride_id}.{ext}')
            print("Decoded selfie image:", selfie_image_file)
        else:
            messages.error(request, "Selfie required to start the ride.")
            return redirect('driver-home')

        # Decode and save the KMS image
        kms_image_file = None
        if kms_image_data:
            format, imgstr = kms_image_data.split(';base64,')
            ext = format.split('/')[-1]
            kms_image_file = ContentFile(base64.b64decode(imgstr), name=f'kms_{ride_id}.{ext}')
            print("Decoded KMS image:", kms_image_file)

        try:
            # Attempt to retrieve the ride with the given ID and driver (ignore the status)
            ride = Ride.objects.get(id=ride_id, driver=request.user.id)
            print(ride)
            
            # Update the ride status to "Started"
            ride.ride_status = "Started"
            
            # Assign the decoded images to the respective fields in the Ride model
            if selfie_image_file:
                ride.selfie = selfie_image_file
            else:
                messages.error(request, 'Selfie Image is mandatory')
                return redirect('driver-home')
            if front_car_image_file:
                ride.Front_pic = front_car_image_file
            else:
                messages.error(request, 'Front Car Image is mandatory')
                return redirect('driver-home')
            
            if back_car_image_file:
                ride.Back_pic = back_car_image_file
            else:
                messages.error(request, 'Back Car Image is mandatory')
                return redirect('driver-home')
            if kms_image_file:
                ride.opening_kms_screen = kms_image_file
            else:
                messages.error(request, 'Kms Image is mandatory')
                return redirect('driver-home')
            if start_kms_input:
                ride.opening_kms_input = start_kms_input
            else:
                messages.error(request, 'Kms Input is mandatory')
                return redirect('driver-home')
            
            ride.save()  # Save the instance with updated fields
            messages.success(request, 'Ride started successfully.')
            return redirect('driver-home')
        except Ride.DoesNotExist:
            messages.error(request, 'Ride not found or you are not authorized to start this ride.')
            return redirect('driver-ongoing')

    messages.error(request, 'Invalid request')
    return redirect('driver-home')


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        print("line 549 :",request.POST)
        # data = request.POST   round(float(ride.fare) * 0.2, 2)
        # amount = request.POST.get('amount')
        ride_id = request.POST.get('ride_id')
        ride_id = decode_hashed_id(ride_id,Ride)
        ride = Ride.objects.get(id = ride_id)
        # print("line 557 :",ride.fare,amount)
        amount = (round(float(ride.fare) * 0.2, 2))* 100  # amount in paise
        print("line 559 :",amount)
        # if int(amount) != expected_amount:
        #     return JsonResponse({'error': 'Invalid amount'}, status=400)
        unique_reference_id = f"{ride_id}-{uuid.uuid4()}"
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            'amount': amount,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })

        # payment_link = client.payment_link.create({
        #     "amount": amount,
        #     "currency": "INR",
        #     "accept_partial": False,
        #     "reference_id": unique_reference_id,
        #     "description": "Payment for your ride with Vaahan",
        #     "customer": {
        #         "name": "Customer Name",
        #         "email": "customer@example.com",
        #         "contact": "9372004279"
        #     },
        #     "notify": {
        #         "sms": True,
        #         "email": True
        #     },
        #     "reminder_enable": True,
        #     "callback_url": "http://127.0.0.1:8000/rides/vendor-rides/",
        #     "callback_method": "get"
        # })
        # send_mail(
        #     subject='Complete Your Ride Payment',
        #     message=f'Please complete your payment for the ride by clicking on the link: {payment_link["short_url"]}',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=['fcgaavez@gmail.com'],
        #     fail_silently=False,
        # )

        # print("Line 568 :",order)
        return JsonResponse(order)

    return HttpResponse(status=405)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        
        # Verify the signature
        data = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        try:
            print("line 587 :",client.utility.verify_payment_signature(data))
            client.utility.verify_payment_signature(data)
            # Payment is verified
            return JsonResponse({'status': 'success'})
        except razorpay.errors.SignatureVerificationError:
            # Invalid signature
            return JsonResponse({'status': 'failure'})
    return JsonResponse({'status': 'error'}, status=400)
@csrf_exempt
def payment_success(request):
    # Handle payment success logic here
    return HttpResponse("Payment successful")

def allRides(reqest):
    if reqest.user.is_authenticated:
        if reqest.user.user_type == 'Admin':
            rides = Ride.objects.all()
            return render(reqest,'adminTemplates/all_rides.html',{"rides":rides})
    raise Http404('Bad Request')

# note: make sure to install this lib 
# sudo apt install wkhtmltopdf -> linux command
# pip install pdfkit -> linux command
# which wkhtmltopdf  # On Linux/MacOS provides the path and paste it in below code

pdfkit_config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

def render_to_pdf(template_src, context_dict):
    # Render the HTML content from template and context
    html = render_to_string(template_src, context_dict)

    # Generate PDF using wkhtmltopdf
    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)  # The `False` means the output is returned as a byte string

    # Create the HTTP response with PDF as an attachment
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="duty_slip.pdf"'
    
    return response

def ride_details_pdf(request, slug):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin':
            # Fetch the ride data
            ride = get_object_or_404(Ride, rideSlug=slug)

            # Prepare the context for the template
            context = {
                'ride': ride
            }

            # Render the template to PDF
            # return render(request,'adminTemplates/duty_slip.html', context) #to test
            return render_to_pdf('adminTemplates/duty_slip.html', context)
    raise Http404("Bad Request")
