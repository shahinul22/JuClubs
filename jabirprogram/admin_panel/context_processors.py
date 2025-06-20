from user.models import User

def all_users(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None

    # Also return all non-superusers as "register_users"
    register_users = User.objects.filter(is_approved=True)

    return {
        'custom_user': user,
        'register_users': register_users
    }
