from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginAdmin, name='loginAdmin'),
    path('logout', views.user_logout, name='logout'),
]