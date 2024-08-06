from django.shortcuts import render

# Create your views here.
def new_car_page(request):

    return render(request,'adminTemplates/new_car.html')

def new_car_type_page(request):
    return render(request,'adminTemplates/new_car_type.html')