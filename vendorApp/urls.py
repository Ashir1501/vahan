from django.urls import path
from .views import *

urlpatterns = [
    path('new-car-page/', new_car_page,name="new-car-page"),
    path('new-car-type-page/', new_car_type_page,name="new-car-type-page"),
   
]