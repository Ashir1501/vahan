from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
# ===============================================================Rides views============================================
            # --------------------Pending Rides Views-------------------------
            
# method to render pending rides page
def Pending_rides_page(request):
    rides_details = Ride.objects.all()
    return render(request,'adminTemplates/ride_details.html',{'ridesData':rides_details})



def autocomplete_driver(request):
    if request:
        query = request.GET.get('term', '')
        if query:
            users = Driver.objects.filter(name__icontains=query) 
        else:
            users = Driver.objects.all()
        print("19 :",users)
        results = []
        for user in users:
            user_json = {
                'id': user.id,
                'label': f"{user.name}",
                'value': user.name,  # This will display in the input box
                
            }
            results.append(user_json)
        print("29 :",results)
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Not an AJAX request'}, status=400)

# method to assign driver
def assign_driver(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        ride_id = request.POST.get('ride_id')
        print("411 :",driver_id)
        if driver_id and ride_id:
            try:
                ride_instance = get_object_or_404(Ride, id=ride_id)
                driver = get_object_or_404(Driver, id=driver_id)
                ride_instance.driver = driver
                if ride_instance.ride_status == 'pending':
                    ride_instance.ride_status = 'assigned'
            except:
                messages.error(request,'Invalid Driver Data')
                return redirect('rides-details-page')
        else:
            messages.error(request,"Invalid Driver Data")
            return redirect('rides-details-page')
        ride_instance.save()
        messages.success(request,f"Ride Assigned to {driver.name}")
        return redirect('rides-details-page')
    redirect('rides-details-page')

            # ---------------------confirmed Views-------------------------------
# method to render ongoing page
def ongoing_rides_page(request):
    rides_details = Ride.objects.all()
    return render(request,'adminTemplates/ongoing.html',{'ridesData':rides_details})

            # -----------------------cancelled Views-------------------------------
def previous_rides_page(request):
    rides_details = Ride.objects.all()
    return render(request,'adminTemplates/previous.html',{'ridesData':rides_details})