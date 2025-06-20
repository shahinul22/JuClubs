from django.utils.deprecation import MiddlewareMixin
from user.models import User

class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Attach a custom user instance (if needed) without overriding request.user.
        Django's AuthenticationMiddleware already handles request.user.
        """
        user_id = request.session.get('user_id')

        if user_id:
            try:
                request.custom_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                request.custom_user = None
        else:
            request.custom_user = None
