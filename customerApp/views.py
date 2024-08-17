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
# Create your views here.
# ===============================================================Rides views============================================
            # --------------------Pending Rides Views-------------------------

def hash_id(objects):
    for obj in objects:
        obj.hashed_id = hashlib.sha256(str(obj.id).encode()).hexdigest()
    return objects
# method to render pending rides page
def Pending_rides_page(request):
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
            print(7555 , car_id)
            if ride_id and driver_id:
                try:
                    ride_instance = get_object_or_404(Ride, id=ride_id)
                    driver = get_object_or_404(Account, id=driver_id)
                    car = get_object_or_404(Car,id = car_id)
                    if Ride.objects.filter(driver=driver, pickup_date=ride_instance.pickup_date).exclude(id=ride_instance.id).exists():
                        messages.error(request, f"The driver {driver} is already assigned to another ride on {ride_instance.pickup_date}.")
                        return redirect('rides-details-page')
                    if Ride.objects.filter(car=car, pickup_date=ride_instance.pickup_date).exclude(id=ride_instance.id).exists():
                        messages.error(request,f"The car {car} is already assigned to another ride on {ride_instance.pickup_date}.")
                        return redirect('rides-details-page')
                    ride_instance.driver = driver
                    ride_instance.car = car
                    
                    if ride_instance.ride_status == 'pending':
                        ride_instance.ride_status = 'confirmed'
                    
                    ride_instance.save()
                    
                    messages.success(request, f"Ride Assigned to {driver.first_name} {driver.last_name} with Car {car.car_model} {car.car_brand}")
                    return redirect('rides-details-page')
                except:
                    messages.error(request, 'Invalid Driver or Ride Data')
                    return redirect('rides-details-page')
            else:
                messages.error(request, 'Invalid Driver or Ride Data')
                return redirect('rides-details-page')
        else:
            messages.error(request, "Invalid Data")
            return redirect('rides-details-page')
        
        return redirect('rides-details-page')
    
    return redirect('rides-details-page')
# method to render ongoing page

def ongoing_rides_page(request):
    rides_details = Ride.objects.all()
    for ride_detail in rides_details:
        ride_detail.hashed_id = hashlib.sha256(str(ride_detail.id).encode()).hexdigest()

    return render(request,'adminTemplates/ongoing.html',{'ridesData':rides_details})

 # -------------------------Completed Ride ----------------------------
def completed_or_past_rides(request):
    today = date.today()
    
    # Filter rides with status 'completed' or with pickup_date in the past
    rides = Ride.objects.filter(
        ride_status='completed'
    ) | Ride.objects.filter(
        pickup_date__lt=today
    )
    for ride_detail in rides:
        ride_detail.hashed_id = hashlib.sha256(str(ride_detail.id).encode()).hexdigest()

    return render(request, 'adminTemplates/previous.html', {'ridesData': rides})


# ---cancel Ride ------- 

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


# HASHED_ID_TO_ORIGINAL_ID = {
#     hashlib.sha256(str(extra.id).encode()).hexdigest(): extra.id
#     for extra in Extra.objects.all()
# }
# @csrf_exempt  
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