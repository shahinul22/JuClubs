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




from clubs.models import RequestedMember
from user.models import User

def join_request_status(request):
    context = {}

    user_id = request.session.get('user_id')
    if not user_id:
        return context

    from clubs.models import Club  # import here to avoid circular error

    # Collect all clubs with pending request by this user
    pending_requests = RequestedMember.objects.filter(
        user_id=user_id,
        is_approved=False,
        is_rejected=False
    ).values_list('club_id', flat=True)

    context['requested_club_ids'] = list(pending_requests)
    return context
