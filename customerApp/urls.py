from django.urls import path
from .views import * 

urlpatterns = [
 # Rides==========
    # Pending Rides-------
    path('rides-details-page',Pending_rides_page,name='rides-details-page'),
    path('assign-driver',assign_driver,name='assign-driver'),
    path('approved-ride',approved_ride,name='approved-ride'),
    # path('autocomplete-driver/', autocomplete_driver, name='autocomplete_driver'),
    # confirmed Rides-----
    path('ongoing-page',ongoing_rides_page,name='ongoing-page'),
    path('extra-page/<str:hashed_id>',extra_page,name='extra-page'),
    # cancelled Rides-----
    path('previous-page',completed_or_past_rides,name='previous-page'),

    path('cancel-ride',cancel_ride,name='cancel-ride'),
    path('add-new-extra/', add_new_extra, name='add-new-extra'),
    path('delete-extra/', delete_Extra, name='delete-extra'),


    path('vendor-rides/', vendor_ride_details, name='vendor-rides'),
    path('confirmed-ride-status/', confirmed_ride_status, name='confirmed_ride_status'),
    path('vendor-suggestions/', vendor_suggestions, name='vendor-suggestions'),


    # path('driver-rides-details/', driver_ride_details, name='driver-rides-details'),
    path('driver-ongoing/', driver_ongoing_details, name='driver-ongoing'),

    path('start-ride/',start_ride, name='start-ride'),

    path('create_order/', create_order, name='create_order'),
    path('payment_success/', payment_success, name='payment_success'),
    path('all-trips/',allRides,name='all-trips-page'),
    path('ride_details_pdf/<slug:slug>/',ride_details_pdf,name='ride_details_pdf'),
]
