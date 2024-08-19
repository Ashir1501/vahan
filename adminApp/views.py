from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usersApp.models import Account
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginAdmin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Account.objects.get(email = email)
        if user.check_password(password):
            auth_login(request,user)
            messages.success(request,f'Welcome {email} You have logged in Successfully.')
            return redirect('adminHome')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'adminTemplates/login.html')

@login_required(login_url='auth/login/')
def user_logout(request):
    logout(request)
    messages.success(request,f'You have logged out')
    return redirect('loginAdmin')