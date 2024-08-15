from django.urls import path
from . import views
urlpatterns = [
    path('',views.adminHome, name='adminHome'),
    path('user-list/',views.userListCreateView.as_view(),name='user-list'),
    path('user/update/<int:pk>',views.updateUser.as_view(),name='user-update'),
    path('user/delete/',views.deleteUser.as_view(),name='user-delete'),
    path('download-aadhar/<int:image_id>/', views.download_aadhar, name='download_aadhar'),
    path('download-driving_licence/<int:image_id>/', views.download_driving_licence, name='download_driving_licence'),
]