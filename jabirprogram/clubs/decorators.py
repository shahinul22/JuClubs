from django.shortcuts import redirect
from functools import wraps
from clubs.models import Club

def club_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        club_id = request.session.get('club_id')
        if not club_id:
            return redirect('clubs:login')  # Adjust name if your login URL name is different

        try:
            request.club = Club.objects.get(id=club_id, is_active=True)
        except Club.DoesNotExist:
            return redirect('clubs:login')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
