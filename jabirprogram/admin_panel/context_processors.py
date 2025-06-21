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


from clubs.models import Club, ClubRegistration

def clubs_context(request):
    approved_clubs = Club.objects.filter(is_active=True)
    pending_clubs = ClubRegistration.objects.filter(is_approved=False)

    return {
        'approved_clubs': approved_clubs,
        'pending_clubs': pending_clubs,
    }
