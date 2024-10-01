from django.shortcuts import render, redirect, get_object_or_404
from usersApp.models import Account, AccountDetail
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.core.files.base import ContentFile
import http.client
import base64
from django.http import Http404
from django.views.decorators.cache import never_cache
from customerApp.models import Ride, Car
import hashlib
import re
from paymentApp.models import *
from django.db.models import Q
# Create your views here.

@login_required(login_url='/auth/admin/login/')
def adminHome(request):
    if request.user.user_type == "Admin":
        return render(request,'adminTemplates/index.html')
    else:
        raise Http404("Page does not exist")
    
def hash_id(objects):
    for obj in objects:
        obj.hashed_id = hashlib.sha256(str(obj.id).encode()).hexdigest()
    return objects

@login_required(login_url='/auth/vendor/login/')
def vendorHome(request):
    if request.user.user_type == "Vendor":
        rides_details = Ride.objects.all()
        drivers = Account.objects.all()
        cars_data = Car.objects.all()
        rides_details = hash_id(rides_details)
        drivers_details = hash_id(drivers)
        cars = hash_id(cars_data)
        for ride in rides_details:
            ride.fare_20_percent = round(float(ride.fare) * 0.2, 2)
        return render(request, 'vendorTemplates/vendors_ride_details.html', {
            'ridesData': rides_details,
            'driverData': drivers_details,
            'cars_data': cars
        })
    else:
        raise Http404("Page does not exist")

@login_required(login_url="/auth/driver/login")
def driverHome(request):
    if request.user.user_type == "Driver":
        rides = Ride.objects.filter(
            Q(driver=request.user.id) & Q(ride_status="assigned")
        )
        print("441  : ",request.user)
        ride_details = []
        # Assuming hash_id function correctly modifies the queryset
        rides = hash_id(rides)

        for ride in rides:
            # Get the payment details for the ride
            payment = Payment.objects.filter(ride=ride).first()  # Get the first payment entry

            # Calculate remaining fare
            if payment and payment.advance_payment is not None and ride.fare is not None:
                remaining_fare = ride.fare - payment.advance_payment
            else:
                remaining_fare = ride.fare if ride.fare is not None else 0

            # Add ride details and payment info
            ride_details.append({
                'ride': ride,
                'advance_payment': payment.advance_payment if payment else None,
                'remaining_fare': remaining_fare
            })

        print("line 454:", ride_details)
        return render(request, 'driverTemplates/driver_ride_details.html', {'rides': ride_details})
    else:
        raise Http404("Page does not exist")

class userListCreateView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Check if the request comes from a Vendor user
            if 'vendor' in request.path:
                return redirect('/auth/vendor/login/')
            else:
                return redirect('/auth/admin/login/')

        # Handle the request if the user is authenticated
        if request.user.user_type == 'Vendor' and 'admin' in request.path:
            raise Http404("Page does not exist")
        if request.user.user_type == 'Admin' and 'vendor' in request.path:
            raise Http404("Page does not exist")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        works_for = Account.objects.filter(user_type__in=['Admin', 'Vendor'])
        gender_choices = AccountDetail.GENDER_CHOICES
        if request.user.user_type=='Admin':
            users = Account.objects.filter(user_type__in=['Driver', 'Vendor','Customer'])
        elif request.user.user_type == 'Vendor':
            account_details = AccountDetail.objects.filter(works_for=request.user)
            users = Account.objects.filter(id__in=account_details.values('user_id'), user_type='Driver')
        else:
            raise Http404("Page does not exist")

        return render(request,'adminTemplates/user_list.html',{'users':users, 'works_for':works_for,'gender_choices':gender_choices})
    
    def post(self, request, *args, **kwargs):
        print("line 102 :",request.headers.get('x-requested-with'))
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = request.POST
            files = request.FILES

            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            password = data.get('password', '').strip()
            if request.user.user_type == 'Vendor':
                 user_type = 'Driver'
                 works_for = request.user.pk
            else:
                user_type = data.get('user_type')
                works_for = data.get('works_for')

            # Extract and strip data from request
            fname = data.get('first_name', '').strip()
            lname = data.get('last_name', '').strip()
            gender = data.get('gender', None)
            join_date = data.get('join_date', '').strip()
            

            # Extract files from request
            photo = files.get('photo', None)
            driving_licence = files.get('driving_licence', None)
            aadhar_card = files.get('aadhar_card', None)

            errors = {}

            # Validate email 
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except ValidationError:
                errors['email'] = "Invalid email format."
            else:
                if Account.objects.filter(email=email).exists():
                    errors['email'] = "Email already exists."

            # Valdate phone number
            if not phone:
                errors['phone'] = "Phone number is required."
            elif not phone.isdigit() or len(phone) != 10:
                errors['phone'] = "Phone number must be exactly 10 digits."
            elif Account.objects.filter(phone_number=phone).exists():
                errors['phone'] = "Phone number already exists."

            # Validate password for Admin
            if user_type == 'Admin' and not password:
                errors['password'] = "Password is required for Admin users."
            
            user = Account()
            user_detail = AccountDetail()
            user_detail.exit_date = None

            user_detail.gender = gender if gender else None
            if(works_for != ""):
                user_detail.works_for = get_object_or_404(Account, pk = works_for)
            else:
                user_detail.works_for = None

            # Validate files
            file_validators = {
                'photo': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png','webp']),
                'driving_licence': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png','webp']),
                'aadhar_card': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png','webp'])
            }

            for file_key in file_validators:
                file = files.get(file_key, None)
                if file:
                    try:
                        file_validators[file_key](file)
                    except ValidationError:
                        errors[file_key] = f"Invalid file type for {file_key.replace('_', ' ')}. Only {', '.join(file_validators[file_key].allowed_extensions)} are allowed."
        

            # Validate dates
            if join_date:
                try:
                    parsed_join_date = parse_date(join_date)
                    if parsed_join_date:
                        user_detail.join_date = parsed_join_date
                    else:
                        errors['join_date'] = "Invalid format for join date."
                except ValueError:
                    errors['join_date'] = "Invalid format for join date."
            print("line 188 : ",errors)
            if errors:
                print("line 190 : ",errors)
                return JsonResponse({'success':False,'error':errors})

            user.first_name = fname if fname else ""
            user.last_name = lname if lname else ""
            user.email = email
            user.phone_number = phone
            user.is_active = False
            user.is_admin = False
            user.is_staff = False
            user.is_superadmin = False
            if user_type == 'Admin':
                user.user_type = Account.CHOICES[1][0]
                user.is_active = True
                user.is_admin = True
                user.is_staff = True
                user.is_superadmin = True
                user.set_password(password)
            elif user_type == 'Vendor':
                user.user_type = Account.CHOICES[0][0]
                user.is_active = True
                user.is_staff = True
            elif user_type =='Driver':
                user.user_type = Account.CHOICES[2][0]
                user.is_active = True
                user.is_staff = True
            user.save()

            if photo:
                user_detail.photo = photo
            
            if driving_licence:
                user_detail.driving_licence = driving_licence
            
            if aadhar_card:
                user_detail.aadhar_card = aadhar_card
            user_detail.user_id = user
            userEmail = request.user.email if request.user.is_authenticated else None
            if userEmail:
                user_detail.created_by = Account.objects.get(email = userEmail)
            else:
                user_detail.created_by = None
                
            user_detail.save()
            return JsonResponse({'success':True})
        return JsonResponse({'success':False, 'error':'Invalid request method'})

def is_valid_password(password):
    # Regex for password validation
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;<>,.?/~]).{8,}$'
    return re.fullmatch(regex, password) is not None

class updateUser(View):
    def post(self,request,*args,**kwargs):
        if request.user.user_type == 'Driver':
            raise Http404("Bad Request")
        pk = kwargs.get('pk')
        account = get_object_or_404(Account, pk = pk)
        data = request.POST
        files = request.FILES

        new_fname = data.get('new_fname','').strip()
        new_lname = data.get('new_lname','').strip()
        new_email = data.get('new_email', '').strip()
        new_phone = data.get('new_phone', '').strip()
        new_gender = data.get('new_gender', None)
        new_join_date = data.get('new_join_date', '').strip()
        new_exit_date = data.get('new_exit_date', '').strip()

        new_photo = files.get('new_photo', None)
        new_driving_licence = files.get('new_driving_licence', None)
        new_aadhar_card = files.get('new_aadhar_card', None)
        if request.user.user_type == 'Vendor':
            new_works_for = request.user.pk
        else:
            new_works_for = data.get('new_works_for', None)

        errors = {}
        accountDetail = account.accountDetail.first()
        if new_gender:
            accountDetail.gender = new_gender
        if(new_works_for):
            if(new_works_for != ''):
                accountDetail.works_for = get_object_or_404(Account, pk = new_works_for)
            

        # Validate new email 
        email_validator = EmailValidator()
        try:
            email_validator(new_email)
        except ValidationError:
            errors['email'] = "Invalid email format."
        else:
            if Account.objects.filter(email=new_email).exclude(pk=account.pk).exists():
                errors['email'] = "Email already exists."

        # Validate new phone number
        if not new_phone:
            errors['phone'] = "Phone number is required."        
        elif not new_phone.isdigit() or len(new_phone) != 10:
            errors['phone'] = "Phone number must be exactly 10 digits."
        elif Account.objects.filter(phone_number=new_phone).exclude(pk=account.pk).exists():
            errors['phone'] = "Phone number already exists."

        if new_join_date:
            try:
                parsed_new_join_date = parse_date(new_join_date)
                if parsed_new_join_date:
                    accountDetail.join_date = parsed_new_join_date
                else:
                    errors['join_date'] = "Invalid format for join date."
            except ValueError:
                errors['join_date'] = "Invalid format for join date."

        if new_exit_date:
            try:
                parsed_new_exit_date = parse_date(new_exit_date)
                if parsed_new_exit_date:
                    accountDetail.exit_date = parsed_new_exit_date
                else:
                    errors['exit_date'] = "Invalid format for exit date."
            except ValueError:
                errors['exit_date'] = "Invalid format for exit date."

        # Validate files
        file_validators = {
            'new_photo': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp']),
            'new_driving_licence': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp']),
            'new_aadhar_card': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp'])
        }

        for file_key in file_validators:
            file = files.get(file_key, None)
            if file:
                try:
                    file_validators[file_key](file)
                except ValidationError:
                    errors[file_key] = f"Invalid file type for {file_key.replace('_', ' ')}. Only {', '.join(file_validators[file_key].allowed_extensions)} are allowed."

        if request.user.user_type == "Admin" and request.path.startswith('/my-profile/update/'):
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            if (new_password) and (not old_password or old_password == ""):
                errors['Password'] = "Please Provide Old Password!!"
            if old_password:
                if new_password:
                    if account.check_password(old_password):
                        if is_valid_password(new_password):
                            account.set_password(new_password)
                            account.save()
                            update_session_auth_hash(request, account)
                        else:
                            errors['Password'] = "New password should atleast have 1 lowercase 1 uppercase, 1 digit, 1 special character and 8 characters long."
                    else:
                        errors['Password'] = "Old Password should match to Update password!!"
                else:
                    errors['Password'] = "Please Provide new Password!!"

        if errors:
            for error, description in errors.items():
                    messages.error(request,f"{description}")
            if request.path.startswith('/my-profile/update/'):
                if request.user.user_type == 'Admin':
                    return redirect('admin-my-profile')
                if request.user.user_type == 'Vendor':
                    return redirect('vendor-my-profile')
                if request.user.user_type == 'Driver':
                    return redirect('driver-my-profile')
            return redirect('user-list')
        
        if new_photo:
            if accountDetail.photo:
                    accountDetail.photo.delete()
            accountDetail.photo = new_photo
        
        if new_driving_licence:
            if accountDetail.driving_licence:
                    accountDetail.driving_licence.delete()
            accountDetail.driving_licence = new_driving_licence
        
        if new_aadhar_card:
            if accountDetail.aadhar_card:
                    accountDetail.aadhar_card.delete()
            accountDetail.aadhar_card = new_aadhar_card
        
        userEmail = request.user.email if request.user.is_authenticated else None
        if userEmail:
            accountDetail.updated_by = get_object_or_404(Account, email = userEmail)
        account.first_name = new_fname if new_fname else ""
        account.last_name = new_lname if new_lname else ""
        account.email = new_email
        account.phone_number = new_phone
        account.save()
        accountDetail.save()

        if request.path.startswith('/my-profile/update/'):
            messages.success(request,"Profile updated successfully")
            if request.user.user_type == 'Admin':
                return redirect('admin-my-profile')
            if request.user.user_type == 'Vendor':
                return redirect('vendor-my-profile')
            if request.user.user_type == 'Driver':
                return redirect('driver-my-profile')
        messages.success(request,"User updated successfully")
        return redirect('user-list')
    
    
class deleteUser(View):
    def get(self, request, *args, **kwargs):
        user_list = request.GET.getlist('user_list[]')
        user_id = request.GET.get('user_id', None)
        if user_id is not None:
            try:
                user_id = int(user_id)
            except ValueError:
                user_id = None

        if user_id:
            try:
                user = Account.objects.get(pk=user_id)
                user_type = user.user_type
                user_detail = AccountDetail.objects.get(user_id = user.pk)
                if user_detail.photo:
                    user_detail.photo.delete()
                if user_detail.aadhar_card:
                    user_detail.aadhar_card.delete()
                if user_detail.driving_licence:
                    user_detail.driving_licence.delete()
                user.delete()

                if user_type == 'Admin':
                    redirect_url = '/admin-home/'
                elif user_type == 'Driver':
                    redirect_url = '/driver-home/'
                elif user_type == 'Vendor':
                    redirect_url = '/vendor-home/'
                else:
                    redirect_url = '/'

                # Return JSON response with redirect URL
                return JsonResponse({'redirect_url': redirect_url})
            except Account.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'User with id {u_id} does not exist'})
        if not user_list:
            return JsonResponse({'success': False, 'error': 'No users selected for deletion'})
        
        for u_id in user_list:
            try:
                user = Account.objects.get(pk=u_id)
                user_detail = AccountDetail.objects.get(user_id = user.pk)
                if user_detail.photo:
                    user_detail.photo.delete()
                if user_detail.aadhar_card:
                    user_detail.aadhar_card.delete()
                if user_detail.driving_licence:
                    user_detail.driving_licence.delete()
                user.delete()
            except Account.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'User with id {u_id} does not exist'})
                
        return JsonResponse({'success':True})

    
def send_otp(request, phone, user_type):
    otp = random.randint(1000, 9999)
    context = {'otp': otp}
    request.session['phone'] = phone

    # conn = http.client.HTTPSConnection("control.msg91.com")
    # headers = { 'Content-Type': "application/JSON" }
    # url = "/api/v5/otp?otp="+otp+"&otp_expiry="+1+"&template_id=&mobile=&authkey=&realTimeResponse="
    # conn.request("POST", url, headers)

    # res = conn.getresponse()
    # data = res.read()

    # print(data.decode("utf-8"))

    if user_type == 'Vendor':
        request.session['vendor_login_otp'] = context
    elif user_type == 'Driver':
        request.session['driver_login_otp'] = context
    return otp

def driver_login(request):
    return vendor_or_driver_login(request, 'Driver')

def vendor_login(request):
    return vendor_or_driver_login(request, 'Vendor')

def resend_otp(request):
    phone = request.session.get('phone')
    user_type = None

    if 'vendor_login_otp' in request.session:
        user_type = 'Vendor'
    elif 'driver_login_otp' in request.session:
        user_type = 'Driver'
    elif 'vendor_registration_data' in request.session:
        user_type = 'Vendor'
    
    if phone and user_type:
        otp = send_otp(request, phone, user_type)
        # print("472 resent otp: ", otp, user_type)
        if 'vendor_registration_data' in request.session:
            request.session.get('vendor_registration_data')['otp'] = otp
        messages.success(request, "OTP has been resent to your phone.")
    else:
        messages.error(request, "Failed to resend OTP.")
    
    return redirect('otp')

def vendor_or_driver_login(request, user_type):
    if request.user.is_authenticated:
        if request.user.user_type == "Driver":
            return redirect('driver-home')
        if request.user.user_type == "Vendor":
            return redirect('vendor-home')
        if request.user.user_type == "Admin":
            return redirect('adminHome')

    if request.method == 'POST':
        phone = request.POST.get('phone', None).strip()
        user = get_object_or_404(Account, phone_number=phone)

        errors = {}
        if not phone:
            errors['phone'] = "Phone number is required."
        elif not phone.isdigit() or len(phone) != 10:
            errors['phone'] = "Phone number must be exactly 10 digits."
        elif user.user_type != user_type:
            errors['phone'] = f"Please Provide Your Phone Number!!"

        if errors:
            for error, description in errors.items():
                messages.error(request, description)
            return redirect(f'{user_type.lower()}_login')

        otp = send_otp(request, phone, user_type)
        # print('line 508 otp: ',otp,user_type)
        return redirect('otp')

    return render(request, f'adminTemplates/{user_type.lower()}_login.html')

def vendor_register(request):
    if request.user.is_authenticated:
        return redirect('vendor-home')
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        email = data.get('email', None).strip()
        phone = data.get('phone', None).strip()
        fname = data.get('fname', None).strip()
        lname = data.get('lname', None).strip()
        gender = data.get('gender', None)
        photo = files.get('photo', None)
        terms_accepted = data.get('terms_check')

        errors = {}

        if not gender:
            errors['Gender'] = 'Please Provide Your Gender'
        if not fname:
            errors['First_Name'] = 'Please provide your First Name'

        if not lname:
            errors['Last_Name'] = 'Please provide your Last Name'
        
        if not terms_accepted:
            errors['terms_and_conditions'] = 'You must accept the terms and conditions.'

        # Validate email 
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors['email'] = "Invalid email format."
        else:
            if Account.objects.filter(email=email).exists():
                errors['email'] = "Email already exists."

        # Validate phone number
        if not phone:
            errors['phone'] = "Phone number is required."
        elif not phone.isdigit() or len(phone) != 10:
            errors['phone'] = "Phone number must be exactly 10 digits."
        elif Account.objects.filter(phone_number=phone).exists():
            errors['phone'] = "Phone number already exists."

        file_validators = {
            'photo': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png','webp']),
        }

        for file_key in file_validators:
            file = files.get(file_key, None)
            if file:
                try:
                    file_validators[file_key](file)
                except ValidationError:
                    errors[file_key] = f"Invalid file type for {file_key.replace('_', ' ')}. Only {', '.join(file_validators[file_key].allowed_extensions)} are allowed."
            else:
                errors['photo'] = "Please Upload photo"

        if errors:
            for error, description in errors.items():
                messages.error(request, description)
            return redirect('vendor_register')

        photo_content = photo.read()
        photo_base64 = base64.b64encode(photo_content).decode('utf-8')
        request.session['vendor_photo_base64'] = photo_base64
        request.session['vendor_photo_name'] = photo.name

        otp = send_otp(request,phone, 'Vendor')
        # print('line 575 otp: ',otp)
        context = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'phone': phone,
            'otp': otp,
            'gender': gender
        }
        request.session['vendor_registration_data'] = context

        return redirect('otp')

    return render(request, 'adminTemplates/vendor_register.html')

@never_cache
def otp(request):
    if request.user.is_authenticated:
        if request.user.user_type == "Driver":
            return redirect('driver-home')
        if request.user.user_type == "Vendor":
            return redirect('vendor-home')
        if request.user.user_type == "Admin":
            return redirect('adminHome')

    phone = request.session.get('phone')
    context = {'phone': phone}
    if request.method == "POST":
        code = request.POST
        if code.get('code_0') and code.get('code_1') and code.get('code_2') and code.get('code_3'):

            otp_entered = int(request.POST.get('code_0') + request.POST.get('code_1') + request.POST.get('code_2') + request.POST.get('code_3'))

            if phone:
                user = Account.objects.filter(phone_number=phone).first()
                if not user:
                    data = request.session.get('vendor_registration_data')
                    if otp_entered == data['otp']:
                        user = Account.objects.create(
                            first_name=data['fname'],
                            last_name=data['lname'],
                            email=data['email'],
                            phone_number=data['phone'],
                            user_type='Vendor',
                            is_staff=True,
                            is_active=True
                        )

                        photo_base64 = request.session.get('vendor_photo_base64')
                        photo_name = request.session.get('vendor_photo_name')

                        if photo_base64:
                            photo_content = base64.b64decode(photo_base64)
                            photo_file = ContentFile(photo_content, photo_name)
                            user_detail = AccountDetail(
                                user_id=user,
                                photo=photo_file,
                                gender=data['gender']
                            )
                            user_detail.save()
                        request.session.pop('vendor_photo_base64', None)
                        request.session.pop('vendor_photo_name', None)
                        request.session.pop('vendor_registration_data', None)
                
                        auth_login(request, user)
                        messages.success(request, f'Welcome {user.email}.')
                        return redirect('vendor-home')
                        # return render(request,'adminTemplates/vendor_stepper.html')
                        # return render(request,'adminTemplates/vendor_workflow.html')
                    else:
                        messages.error(request, "Invalid OTP")
                        return redirect('otp')

                if user.user_type == 'Vendor':
                    data = request.session.get('vendor_login_otp')
                    if data:
                        if otp_entered == data['otp']:
                            auth_login(request, user)
                            messages.success(request, f'Welcome {user.email}.')
                            request.session.pop('vendor_login_otp', None)
                            return redirect('vendor-home')
                        else:
                            messages.error(request, "Invalid OTP")
                            return redirect('otp')
                    else:
                        raise Http404("Bad Request")

                if user.user_type == 'Driver':
                    data = request.session.get('driver_login_otp')
                    if data:
                        if otp_entered == data['otp']:
                            auth_login(request, user)
                            messages.success(request, f'Welcome {user.email}.')
                            request.session.pop('driver_login_otp', None)
                            return redirect('driver-home')
                        else:
                            messages.error(request, "Invalid OTP")
                            return redirect('otp')
                    else:
                        raise Http404("Bad request")
        else:
            messages.error(request, "Provide OTP")
            return redirect('otp')
    # start temporary otp alert pop up on user interface
    otp_data = None
    if 'vendor_registration_data' in request.session and request.session['vendor_registration_data'] and 'otp' in request.session['vendor_registration_data']:
        otp_data = request.session['vendor_registration_data']['otp']
    elif 'vendor_login_otp' in request.session and request.session['vendor_login_otp'] and 'otp' in request.session['vendor_login_otp']:
        otp_data = request.session['vendor_login_otp']['otp']
    elif 'driver_login_otp' in request.session and request.session['driver_login_otp'] and 'otp' in request.session['driver_login_otp']:
        otp_data = request.session['driver_login_otp']['otp']

    if otp_data:
        messages.success(request, f'OTP is {otp_data}.')
    else:
        messages.error(request, 'No OTP.')
    # end temp otp alert code 

    return render(request, 'adminTemplates/otp.html', context)


def myProfile(request):
    users = Account.objects.all()
    works_for = Account.objects.filter(user_type__in=['Admin', 'Vendor'])
    gender_choices = AccountDetail.GENDER_CHOICES
    return render(request,'adminTemplates/my_profile.html',{'users':users, 'works_for':works_for,'gender_choices':gender_choices})

