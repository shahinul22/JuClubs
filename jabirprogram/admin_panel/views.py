from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import User

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_panel:admin_dashboard_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_panel:admin_dashboard_view')
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'admin_panel/login.html')


@login_required
def admin_dashboard_view(request):
    return render(request, 'admin_panel/dashboard.html')

@login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_panel:admin_login_view')
def admin_logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('admin_panel:admin_login_view')

from django.shortcuts import get_object_or_404, redirect
from user.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_panel:admin_login_view')
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_panel:admin_dashboard_view')
