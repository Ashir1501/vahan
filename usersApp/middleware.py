from django.utils.deprecation import MiddlewareMixin
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CleanUpSessionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only run the cleanup if registration was in progress and not completed
        if request.session.get('registration_in_progress') and not request.session.get('vendor_registration_complete'):
            # Check if the registration page was the last visited
            if request.path not in ['/vendor_register/', '/otp/']:
                # If the user navigates away or closes the browser during registration,
                # clean up the photo and session data
                photo_path = request.session.get('vendor_photo_path')
                if photo_path:
                    print('line 15 midd')
                    fs = FileSystemStorage(location=settings.USER_MEDIA_ROOT)
                    fs.delete(photo_path.replace(settings.USER_MEDIA_URL, ''))

                    # Clean up session data
                    request.session.pop('vendor_photo_path', None)
                    request.session.pop('registration_in_progress', None)
                    request.session.pop('vendor_registration_data', None)

        return response
