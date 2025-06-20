from .models import User

def user_context(request):
    user_obj = None
    if request.session.get('user_id'):
        try:
            user_obj = User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            pass
    return {
        'logged_user': user_obj
    }
