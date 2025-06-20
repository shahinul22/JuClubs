# admin_panel/context_processors.py
from user.models import User

def all_users(request):
    if request.user.is_authenticated:
        return {'register_users': User.objects.all()}  # or filter by your own criteria
    return {}


