from django.shortcuts import render, redirect, get_object_or_404
from usersApp.models import Account, AccountDetail
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.contrib.auth import login as auth_login, logout
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.

@login_required(login_url='/auth/admin/login/')
def adminHome(request):
    return render(request,'adminTemplates/index.html')

@login_required(login_url='/auth/vendor/login/')
def vendorHome(request):
    return render(request,'adminTemplates/index.html')

@login_required(login_url="/auth/driver/login")
def driverHome(request):
    return render(request,'adminTemplates/index.html')

class userListCreateView(LoginRequiredMixin,View):
    login_url = '/auth/admin/login/'
    def get(self, request):
        users = Account.objects.all()
        works_for = Account.objects.filter(user_type__in=['Admin', 'Vendor'])
        gender_choices = AccountDetail.GENDER_CHOICES
        return render(request,'adminTemplates/user_list.html',{'users':users, 'works_for':works_for,'gender_choices':gender_choices})
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = request.POST
            files = request.FILES

            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            password = data.get('password', '').strip()
            user_type = data.get('user_type')

            # Extract and strip data from request
            fname = data.get('first_name', '').strip()
            lname = data.get('last_name', '').strip()
            gender = data.get('gender', None)
            join_date = data.get('join_date', '').strip()
            works_for = data.get('works_for')

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
                user_detail.works_for = Account.objects.get(pk = works_for)
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

            if errors:
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
                user_detail.updated_by = Account.objects.get(email = userEmail)
            else:
                user_detail.updated_by = None
                
            user_detail.save()
            return JsonResponse({'success':True})
        return JsonResponse({'success':False, 'error':'Invalid request method'})

class updateUser(View):
    def post(self,request,*args,**kwargs):
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
        new_works_for = data.get('new_works_for', None)

        errors = {}
        accountDetail = account.accountDetail.first()
        accountDetail.gender = new_gender if new_gender else None
        if(new_works_for):
            if(new_works_for != ''):
                accountDetail.works_for = Account.objects.get(pk = new_works_for)
        else:
            accountDetail.works_for = None
            

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

        if errors:
            for error, description in errors.items():
                    messages.error(request,f"{description}")
            return redirect('user-list')
        
        if new_photo:
            accountDetail.photo = new_photo
        
        if new_driving_licence:
            accountDetail.driving_licence = new_driving_licence
        
        if new_aadhar_card:
            accountDetail.aadhar_card = new_aadhar_card
        
        userEmail = request.user.email if request.user.is_authenticated else None
        if userEmail:
            accountDetail.updated_by = Account.objects.get(email = userEmail)
        else:
            accountDetail.updated_by = None
        account.first_name = new_fname if new_fname else ""
        account.last_name = new_lname if new_lname else ""
        account.email = new_email
        account.phone_number = new_phone
        account.save()
        accountDetail.save()
        messages.success(request,"User updated successfully")
        return redirect('user-list')
    
    
class deleteUser(View):
    def get(self, request, *args, **kwargs):
        user_list = request.GET.getlist('user_list[]')

        if not user_list:
            return JsonResponse({'success': False, 'error': 'No users selected for deletion'})
        
        for user_id in user_list:
            try:
                user = Account.objects.get(pk=user_id)
                user.delete()
            except Account.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'User with id {user_id} does not exist'})
                
        return JsonResponse({'success':True})

def download_aadhar(request, image_id):
    account_detail = get_object_or_404(AccountDetail, id=image_id)
    image_path = account_detail.aadhar_card.path

    with default_storage.open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{account_detail.aadhar_card.name}"'
        return response

def download_driving_licence(request, image_id):
    account_detail = get_object_or_404(AccountDetail, id=image_id)
    image_path = account_detail.driving_licence.path

    with default_storage.open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{account_detail.driving_licence.name}"'
        return response
    
def send_otp(request, phone, user_type):
    otp = random.randint(1000, 9999)
    context = {'otp': otp}
    request.session['phone'] = phone
    if user_type == 'Vendor':
        request.session['vendor_login_otp'] = context
    elif user_type == 'Driver':
        request.session['driver_login_otp'] = context
    return otp

def driver_login(request):
    return vendor_or_driver_login(request, 'Driver')

def vendor_login(request):
    return vendor_or_driver_login(request, 'Vendor')

def vendor_or_driver_login(request, user_type):
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
        print('line 351 otp: ',otp)
        return redirect('otp')

    return render(request, f'adminTemplates/{user_type.lower()}_login.html')

def vendor_register(request):
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

        fs = FileSystemStorage(location=settings.USER_MEDIA_ROOT)
        photo_name = fs.save(photo.name, photo)
        photo_path = f'{settings.USER_MEDIA_URL}{photo_name}'

        otp = send_otp(request,phone, 'Vendor')
        print('line 415 otp: ',otp)
        context = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'phone': phone,
            'otp': otp,
            'photo_path': photo_path,
            'gender': gender
        }
        request.session['vendor_registration_data'] = context
        request.session['vendor_photo_path'] = photo_path
        # request.session['registration_in_progress'] = True
        return redirect('otp')

    return render(request, 'adminTemplates/vendor_register.html')

def otp(request):
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
                            OTP=data['otp'],
                            user_type='Vendor',
                            is_staff=True,
                            is_active=True
                        )
                        user_detail = AccountDetail(
                            user_id=user,
                            photo=data['photo_path'],  # Assign the path saved in user_images
                            gender=data['gender']
                        )
                        user_detail.save()

                        # request.session['vendor_registration_complete'] = True
                        # request.session.pop('registration_in_progress', None)

                        # Clear the session data after successful registration
                        request.session.pop('vendor_photo_path', None)
                        request.session.pop('vendor_registration_data', None)

                        auth_login(request, user)
                        messages.success(request, f'Welcome {user.email} You have Registered Successfully.')
                        return redirect('vendor-home')
                    else:
                        #this below code deletes the photo if the user fails to register
                        # if 'photo_path' in data:
                        #     fs = FileSystemStorage(location=settings.USER_MEDIA_ROOT)
                        #     fs.delete(data['photo_path'].replace(settings.USER_MEDIA_URL, ''))
                        messages.error(request, "Invalid OTP")
                        return redirect('otp')

                if user.user_type == 'Vendor':
                    data = request.session.get('vendor_login_otp')
                    if otp_entered == data['otp']:
                        auth_login(request, user)
                        messages.success(request, f'Welcome {user.email} You have logged in Successfully.')
                        return redirect('vendor-home')
                    else:
                        messages.error(request, "Invalid OTP")
                        return redirect('otp')

                if user.user_type == 'Driver':
                    data = request.session.get('driver_login_otp')
                    if otp_entered == data['otp']:
                        auth_login(request, user)
                        messages.success(request, f'Welcome {user.email} You have logged in Successfully.')
                        return redirect('vendor-home')
                    else:
                        messages.error(request, "Invalid OTP")
                        return redirect('otp')
        else:
            messages.error(request, "Provide OTP")
            return redirect('otp')
    return render(request, 'adminTemplates/otp.html', context)
