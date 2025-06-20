from django.shortcuts import redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not getattr(request, 'user', None):
            return redirect('user:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
