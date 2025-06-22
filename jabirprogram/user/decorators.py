from django.shortcuts import redirect
from functools import wraps
# user/decorators.py
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def user_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page")
            return redirect('user:login')  # Change to your login URL name
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.shortcuts import redirect
from functools import wraps

def login_redirect_home(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')  # your home URL name here
        return function(request, *args, **kwargs)
    return wrap
