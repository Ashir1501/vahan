from django.urls import path
from .views import *

urlpatterns = [
    # Cars urls--------
    path('new-car-page/', new_car_page,name="new-car-page"),
    path('new-car-type-page/', new_car_type_page,name="new-car-type-page"),
    path('add-new-car',add_new_car,name='add-new-car'),
    path('car_model_search/', car_model_search, name='car_model_search'),
    # path('car_type_add',car_type_add,name="car_type_add"),
    path('edit-car/', edit_car, name='edit_car'),
    path('delete-car/', delete_car, name='delete-car'),
    # Cars Type Urls-------
    path('add-car-type/', create_car_type, name='add-car-type'),
    path('car-type-edit/', update_car_type, name='car-type-edit'),
    path('delete-car-type/', delete_car_type, name='delete-car-type'),
    # Routes urls--------
    path('routes-page',Routes_page,name='routes-page'),
    path('add-route/', add_route, name='add-route'),
    path('edit-routes',edit_route,name='edit-routes'),
    path('delete-route',delete_route,name='delete-route'),

    path('carType_suggestions',carType_suggestions,name='carType_suggestions'),
  
]