from django.urls import path
from .views import *
urlpatterns = [
    path('paymen-proceed/<str:hashed_id>',ride_payment, name='paymen-proceed'),
    path('callback/',payment_callback,name='callback'),
    path('payment-page/',Payment_page,name='payment-page')

]