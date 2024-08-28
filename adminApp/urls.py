from django.urls import path
from . import views
urlpatterns = [
    path('admin/login/',views.loginAdmin, name='loginAdmin'),
    path('logout', views.user_logout, name='logout'),
]