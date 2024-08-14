from django.shortcuts import render, redirect, get_object_or_404
from usersApp.models import Account, AccountDetail
from django.views.generic import View
from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.validators import FileExtensionValidator

# Create your views here.
def adminHome(request):
    return render(request,'adminTemplates/index.html')

class userListCreateView(View):
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
                'photo': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                'driving_licence': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
                'aadhar_card': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])
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
        account = get_object_or_404(Account, pk = kwargs.get('pk'))
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
        new_works_for = data.get('new_works_for')

        errors = {}
        accountDetail = account.accountDetail.first()
        accountDetail.gender = new_gender if new_gender else None
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
            'new_photo': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            'new_driving_licence': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            'new_aadhar_card': FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])
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