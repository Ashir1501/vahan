from django.apps import AppConfig


class UsersappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersApp'

    def ready(self):
        import usersApp.signals