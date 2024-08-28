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
]
