from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

User = get_user_model()

@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    # Define permissions for each group
    permissions_mapping = {
        'Admin': ['add_account', 'change_account', 'delete_account', 'view_account', 'add_accountdetail', 'change_accountdetail', 'delete_accountdetail', 'view_accountdetail', 'add_cartype', 'change_cartype', 'delete_cartype', 'view_cartype', 'add_route', 'change_route', 'delete_route', 'view_route', 'add_car', 'change_car', 'delete_car', 'view_car', 'add_ride', 'change_ride', 'view_ride', 'delete_ride', 'add_extra', 'view_extra', 'add_payment', 'view_payment'],
        'Vendor': ['add_account', 'change_account', 'delete_account', 'view_account', 'add_accountdetail', 'change_accountdetail', 'delete_accountdetail', 'view_accountdetail', 'add_cartype', 'change_cartype', 'delete_cartype', 'view_cartype', 'add_route', 'change_route', 'delete_route', 'view_route', 'add_car', 'change_car', 'delete_car', 'view_car', 'add_ride', 'view_ride', 'delete_ride', 'add_extra', 'view_extra', 'add_payment', 'view_payment'],
        'Driver': ['add_account', 'view_account', 'change_account', 'delete_account', 'add_accountdetail', 'change_accountdetail', 'delete_accountdetail', 'view_accountdetail', 'view_cartype', 'view_route', 'view_car', 'change_ride', 'view_ride', 'add_extra', 'view_extra', 'view_payment'],
        'Customer': ['add_account', 'change_account', 'delete_account', 'view_account', 'add_accountdetail', 'view_cartype', 'view_route', 'view_car', 'view_ride', 'view_extra', 'add_extra', 'view_payment', 'add_payment']
    }

    for group_name, permissions_list in permissions_mapping.items():
        # Get or create the group
        group, created = Group.objects.get_or_create(name=group_name)

        # Assign permissions to the group
        permissions = Permission.objects.filter(codename__in=permissions_list)
        group.permissions.set(permissions)


@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        user = instance
        user_type = user.user_type

        # Define group mapping based on user type
        group_name = None
        if user_type == 'Vendor':
            group_name = 'Vendor'
        elif user_type == 'Admin':
            group_name = 'Admin'
        elif user_type == 'Driver':
            group_name = 'Driver'
        elif user_type == 'Customer':
            group_name = 'Customer'

        # Assign user to the appropriate group if group exists
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
