from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usersApp.models import Account
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

def loginAdmin(request):
    if request.user.is_authenticated:
        return redirect('adminHome')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = get_object_or_404(Account, email=email)
        if user.check_password(password):
            auth_login(request,user)
            messages.success(request,f'Welcome {email} You have logged in Successfully.')
            return redirect('adminHome')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'adminTemplates/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        logout(request)
        messages.success(request,f'You have logged out')
        if user_type == 'Admin':
            return redirect('loginAdmin')
        elif user_type == 'Vendor':
            return redirect('vendor_login')
        else:
            return redirect('driver_login')
    else:
        raise Http404("Bad request")