from django.urls import path
from . import views
urlpatterns = [
    path('admin-home/',views.adminHome, name='adminHome'),
    path('admin-home/user-list/',views.userListCreateView.as_view(),name='user-list'),
    path('user/update/<int:pk>',views.updateUser.as_view(),name='user-update'),
    path('user/delete/',views.deleteUser.as_view(),name='user-delete'),
    path('vendor-home/',views.vendorHome,name='vendor-home'),
    path('driver-home/',views.driverHome,name='driver-home'),
    path('auth/vendor/login/', views.vendor_login, name='vendor_login'),
    path('auth/driver/login/', views.driver_login, name='driver_login'),
    path('vendor/register/',views.vendor_register,name='vendor_register'),
    path('otp',views.otp,name='otp'),
    path('resend_OTP/', views.resend_otp, name='resend_OTP'),
    path('admin-home/my-profile/',views.myProfile,name='admin-my-profile'),
    path('vendor/my-profile/',views.myProfile,name='vendor-my-profile'),
    path('driver/my-profile/',views.myProfile,name='driver-my-profile'),
    path('my-profile/update/<int:pk>',views.updateUser.as_view(),name='my-profile-update'),
    path('vendor/driver-list/',views.userListCreateView.as_view(),name='vendor-driver-list'),
]