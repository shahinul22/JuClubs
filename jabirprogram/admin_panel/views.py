from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import User
from user.decorators import user_login_required
from clubs.decorators import club_login_required

@club_login_required
def club_profile_tab_view(request, tab='about'):
    club = request.club  # club is set in the decorator
    ...


@user_login_required
def club_profile_tab_view(request, tab='about'):
    ...

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


from clubs.models import Club

@login_required
def admin_dashboard_view(request):
    approved_clubs = Club.objects.filter(is_active=True)
    # Pass approved_clubs in the context
    return render(request, 'admin_panel/dashboard.html', {'approved_clubs': approved_clubs})

@login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_panel:admin_login_view')
def admin_logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('admin_panel:admin_login_view')

from django.shortcuts import get_object_or_404, redirect
from user.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

# @login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_panel:admin_login_view')
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_panel:admin_dashboard_view')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from clubs.models import ClubRegistration

@login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser)
def pending_club_list_view(request):
    pending_clubs = ClubRegistration.objects.filter(is_approved=False)
    return render(request, 'admin_panel/pending_clubs.html', {'pending_clubs': pending_clubs})

from django.db import IntegrityError
from django.contrib.auth.models import User
from clubs.models import Club, Member, ClubRegistration
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
@login_required(login_url='admin_panel:admin_login_view')
@user_passes_test(lambda u: u.is_superuser)
def approve_club_view(request, reg_id):
    registration = get_object_or_404(ClubRegistration, id=reg_id, is_approved=False)
    registration.approve()
    messages.success(request, f"Club '{registration.club_name}' approved successfully.")
    return redirect('admin_panel:pending_list')