from django.urls import path
from .views import * 

urlpatterns = [
 # Rides==========
    # Pending Rides-------
    path('rides-details-page',Pending_rides_page,name='rides-details-page'),
    path('assign-driver',assign_driver,name='assign-driver'),
    path('autocomplete-driver/', autocomplete_driver, name='autocomplete_driver'),
    # confirmed Rides-----
    path('ongoing-page',ongoing_rides_page,name='ongoing-page'),
    # cancelled Rides-----
    path('previous-page',previous_rides_page,name='previous-page'),
]
