from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import CarType
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from PIL import Image
from .models import *
from usersApp.models import *
from customerApp.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
# =================Cars Views=====================
# new Car page 
@login_required(login_url='auth/login/')
def new_car_page(request):
    data = Car.objects.all()
    TypeData = CarType.objects.all()
    car_ids = Ride.objects.filter(ride_status='Started').values_list('car', flat=True).distinct()
    unique_car_types = []
    seen_car_types = set()
    
    for car_type in TypeData:
        if car_type.car_type not in seen_car_types:
            unique_car_types.append(car_type)
            seen_car_types.add(car_type.car_type)
    Vendor = Account.objects.all()
    return render(request,'adminTemplates/new_car.html',{'data':data,'CarsType':unique_car_types,'vendorData':Vendor,"notAvalaibe":car_ids})

# method to create new cars
@login_required(login_url='auth/login/')
def add_new_car(request):
    if request.method == 'POST':
        car_type_id = request.POST.get("carsTypeId")
        car_brand = request.POST.get("carBrand")
        car_model = request.POST.get("carModel")
        vendor_id = request.POST.get("vendorId")
        registration_number = request.POST.get("registrationNumber")

        # Handle file uploads
        front_pic = request.FILES.get("frontPic")
        back_pic = request.FILES.get("backPic")
        rc_photo = request.FILES.get("rcPhoto")

        # Validate image files
        for image, image_name in zip([front_pic, back_pic, rc_photo], ['Front Pic', 'Back Pic', 'RC Photo']):
            if image:
                try:
                    img = Image.open(image)
                    img.verify()
                except:
                    messages.error(request, f"{image_name} must be an image.")
                    return redirect('new-car-page')
            elif image_name == 'RC Photo':
                messages.error(request, "RC Photo is required.")
                return redirect('new-car-page')

        try:
            # Retrieve or create the CarType
            car_type, created = CarType.objects.get_or_create(car_type=car_type_id)
            if created:
                messages.success(request, "Car Type added to the system.")

            # Retrieve the vendor
            if vendor_id == 'me':
                vendor = Account.objects.get(id=1)
            else:
                vendor = Account.objects.get(id=vendor_id)

            # Create new car instance
            new_car = Car(
                Car_type=car_type,
                car_brand=car_brand,
                car_model=car_model,
                Vender_id=vendor,
                Front_pic=front_pic,
                Back_pic=back_pic,
                Registration_Number=registration_number,
                rc_photo=rc_photo,
                is_available=True,  # Set this according to your needs
                created_by=Account.objects.get(id=1)  # Adjust according to your logic
            )
            new_car.save()

            # Redirect after successful save
            messages.success(request, "Data added successfully.")
            return redirect('new-car-page')

        except Account.DoesNotExist:
            messages.error(request, "Vendor does not exist.")
            return redirect('new-car-page')

    else:
        # Handle GET request or other methods
        return render(request, 'new_car.html')
# method to search car type and show in car type input to get
@login_required(login_url='auth/login/')
def car_model_search(request):
    query = request.GET.get('query', '')
    car_type = CarType.objects.filter(car_type__icontains=query)
    results = [{'id': cm.id, 'name': cm.car_type} for cm in car_type]
    return JsonResponse({'results': results})


# method to edit car 
@login_required(login_url='auth/login/')
@require_POST
def edit_car(request):
    print("1111111111222222220")
    if request.method == 'POST':
        print("hii1212")
        car_id = request.POST.get('car_id')
        car = get_object_or_404(Car, id=car_id)

        # Get form data
        car_model = request.POST.get('car_model_edit')
        car_type_query = request.POST.get('car_type_edit')
        car_brand = request.POST.get('car_brand_edit')
        registration_number = request.POST.get('registration_number_edit')

        # Query for CarType using filter
        car_types = CarType.objects.filter(car_type__icontains=car_type_query)

        if not car_types.exists():
            messages.error(request, f'The car type "{car_type_query}" is not present in your system. Please add it before proceeding.')

            return redirect('new-car-page')

        # Assuming the filter returns a single unique result, you can use first() or handle the case where multiple results exist
        carT = car_types.first()

        # Update car instance
        car.car_model = car_model
        car.Car_type = carT
        car.car_brand = car_brand
        car.Registration_Number = registration_number

        # Handle file uploads
        if 'front_pic_edit' in request.FILES:
            car.Front_pic = request.FILES['front_pic_edit']
            try:
                img1 = Image.open(request.FILES['front_pic_edit'])
                img1.verify()
            except:
                messages.error(request,"File Must be image")
                return redirect('new-car-page')       

        if 'back_pic_edit' in request.FILES:
            car.Back_pic = request.FILES['back_pic_edit']
            try:
                img2 = Image.open(request.FILES['back_pic_edit'])
                img2.verify()
            except:
                messages.error(request,"File Must be image")
                return redirect('new-car-page')
        
        if 'rc_pic_edit' in request.FILES:
            car.rc_photo = request.FILES['rc_pic_edit']
            try:
                img3 = Image.open(request.FILES['rc_pic_edit'])
                img3.verify()
            except:
                messages.error(request,"File Must be image")
                return redirect('new-car-page')
        
        car.is_available = 'available_check' in request.POST
        car.save()

        messages.success(request, f'Car details for "{car_model}" have been updated successfully!')
        return redirect('new-car-page')

    else:
        messages.error(request, 'Invalid request method.')
        return redirect('new-car-page')


# method to delete car data
@login_required(login_url='auth/login/')
@csrf_exempt  
def delete_car(request):
    if request.method == 'POST':
        car_ids = request.POST.getlist('car_ids[]')  # Get the list of car IDs
        print("Car IDs to delete:", car_ids)

        try:
            # Use filter to delete all cars with the provided IDs
            cars = Car.objects.filter(id__in=car_ids)
            deleted_count, _ = cars.delete()  # Delete the cars and get the count of deleted items
            
            if deleted_count > 0:
                return JsonResponse({'success': True, 'deleted_count': deleted_count})
            else:
                return JsonResponse({'success': False, 'error': 'No cars found to delete'}, status=404)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

# this method for add new car type from cars form
def car_type_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            car_model, created = CarType.objects.get_or_create(car_type=name)
            if created:
                return JsonResponse({'id': car_model.id, 'name': car_model.car_type})
            else:
                return JsonResponse({'error': 'Car model already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Name is required'}, status=400)
        


# ==================Cars Type Views===============================================
# method for render new car type page
@login_required(login_url='auth/login/')
def new_car_type_page(request):
    car_type_data = CarType.objects.annotate(car_count=Count('car'))

    return render(request, 'adminTemplates/new_car_type.html', {'carType': car_type_data})


# method to cerate new car type
def create_car_type(request):
    print(2222555)
    if request.method == 'POST':
        car_type_name = request.POST.get('car_types')
        print("228 :",car_type_name)
        if car_type_name:
            check = CarType.objects.filter(car_type__icontains = car_type_name)
            print(231,check)
            if not check:
                CarType.objects.create(car_type=car_type_name)
                messages.success(request, 'Type Added successfully!')
                return redirect('new-car-type-page')
            else:
                messages.error(request, f"'{car_type_name}' is already present")
                return redirect('new-car-type-page')
        return redirect('new-car-type-page')
    return redirect('new-car-type-page')

# method to update car type
def update_car_type(request):
    car_type_id = request.POST.get('car_type_id')
    car_type = get_object_or_404(CarType, id=car_type_id)

    if request.method == 'POST':
        car_type_name = request.POST.get('car_type_edit')
        if car_type_name:
            car_type.car_type = car_type_name
            car_type.save()
            messages.success(request, 'Type Update successfully!')
            return redirect('new-car-type-page')  # Redirect to a list of car types or another page

    return render(request, 'adminTemplates/new_car_type.html', {'car_type': car_type})


# method to delete car type
@require_POST
def delete_car_type(request):


    if request.method == 'POST':
        car_type_ids = request.POST.getlist('car_type_ids[]')  # Get the list of car IDs
        print("Car IDs to delete:", car_type_ids)

        try:
            # Use filter to delete all cars with the provided IDs
            cars_type = CarType.objects.filter(id__in=car_type_ids)
            deleted_count, _ = cars_type.delete()  # Delete the cars and get the count of deleted items
            
            if deleted_count > 0:
                return JsonResponse({'success': True, 'deleted_count': deleted_count})
            else:
                return JsonResponse({'success': False, 'error': 'No cars found to delete'}, status=404)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# ===========================================Routes Views=============================

# method to render Routes page
@login_required(login_url='auth/login/')
def Routes_page(request):
    routes_data = Route.objects.all()
    cartype= CarType.objects.all()
    return render(request,'adminTemplates/Route.html',{'routeData':routes_data,'CarsType':cartype})


# method to add new route
@login_required(login_url='auth/login/')
def add_route(request):
    if request.method == 'POST':
        trip_type = request.POST.get('tripType')
        pickup_location = request.POST.get('pickup')
        drop_location = request.POST.get('DropOff')
        fare = request.POST.get('fare')
        duration = request.POST.get('duration')
        kms = request.POST.get('Kilometers')
        car_type_ids = request.POST.get('carsTypeId')  # Handle multiple car types
        
        # Validation
        if not pickup_location  or not fare:
            # return HttpResponse("Missing required fields", status=400)
            messages.error(request,"Missing required fields")
            return redirect('routes-page')
        if trip_type == 'local':
            if duration == 'none':
                messages.error(request, "If the route type is 'Local', then 'Duration' is required.")
                return redirect('routes-page')
        else:  # trip_type is not 'local'
            if duration != 'none':
                messages.error(request, "If the route type is not 'Local', then 'Duration' should not be provided.")
                return redirect('routes-page')
            if kms and int(kms) < 0 and trip_type != 'local':
                messages.error(request, "KMS value must be a non-negative number.")
                return redirect('routes-page')
        try:
            car_type, created = CarType.objects.get_or_create(car_type=car_type_ids)
        except:
            pass
        if created:
                messages.success(request, "Car Type added to the system.")
        try:
            fare = float(fare)
            if trip_type != 'local':
                kms = int(kms)
            else:
                kms =0 
        except ValueError:
            messages.error(request,"Invalid fare or kilometers")
            return redirect('routes-page')
            # return HttpResponse("Invalid fare or kilometers", status=400)

        route = Route(
            trip_type=trip_type,
            car_type = car_type,
            pickup_location=pickup_location,
            drop_location=drop_location,
            fare=fare,
            duration=duration,
            kms=kms,
            created_by=Account.objects.get(id=1)             #request.user.account  # Or however you determine the creator
        )
        route.save()
        
        # Handle ManyToManyField for CarType

        # try :
        #         matching_car_types = CarType.objects.filter(car_type__icontains=car_type_ids)
        #         route.car_type.add(*matching_car_types)
        # except:
        #     messages.error(request,"This car Type is not present in your System")
        #     return redirect('routes-page')

        messages.success(request,"Routes Added Successfully!")
        return redirect('routes-page')  # Redirect to a success page or wherever you want
    else:
        return render(request, 'Routes.html')

# method to edit routes
@login_required(login_url='auth/login/')
def edit_route(request):
    

    if request.method == 'POST':
        # Extract data from the POST request
        route = get_object_or_404(Route, id=request.POST.get('routeId'))
        trip_type = request.POST.get('tripTypeEdit')
        pickup_location = request.POST.get('pickupEdit')
        drop_location = request.POST.get('dropOffEdit')
        car_type = request.POST.get('carType')
        fare = request.POST.get('fareEdit')
        kms = request.POST.get('kmsEdit')
        duration = request.POST.get('duration')

        # Validate and process the data
        if not all([trip_type, pickup_location, car_type, fare]):
            messages.error(request,"Missing required fields")
            return redirect('routes-page')
        car_types = CarType.objects.filter(car_type__icontains=car_type)

        if not car_types.exists():
            messages.error(request, f'The car type "{car_type}" is not present in your system. Please add it before proceeding.')

            return redirect('routes-page')

        # Assuming the filter returns a single unique result, you can use first() or handle the case where multiple results exist
        carT = car_types.first()
        if trip_type == 'local':
            if duration == 'none':
                messages.error(request, "If the route type is 'Local', then 'Duration' is required.")
                return redirect('routes-page')
        else:  # trip_type is not 'local'
            if duration != 'none':
                messages.error(request, "If the route type is not 'Local', then 'Duration' should not be provided.")
                return redirect('routes-page')
            if kms and int(kms) < 0:
                messages.error(request, "KMS value must be a non-negative number.")
                return redirect('routes-page')
        # Update route data
        route.trip_type = trip_type
        route.pickup_location = pickup_location
        route.drop_location = drop_location
        route.car_type = carT # Assuming car_type is a ManyToManyField
        route.fare = fare
        route.kms = kms
        route.duration = duration

        # Save the updated route object
        route.save()

        # Redirect to a success page or the same page
        messages.success(request,"Route Update Successfully")
        return redirect('routes-page')

    else:
        # Render the form if it's not a POST request
        return redirect('routes-page')
    
# method to delete routes
@require_POST
@login_required(login_url='auth/login/')
def delete_route_type(request):


    if request.method == 'POST':
        route_ids = request.POST.getlist('routes_ids[]')  # Get the list of car IDs
        print("Car IDs to delete:", route_ids)

        try:
            # Use filter to delete all cars with the provided IDs
            Routes = Route.objects.filter(id__in=route_ids)
            deleted_count, _ = Routes.delete()  # Delete the cars and get the count of deleted items
            
            if deleted_count > 0:
                return JsonResponse({'success': True, 'deleted_count': deleted_count})
            else:
                return JsonResponse({'success': False, 'error': 'No cars found to delete'}, status=404)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)



