from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import ClubRegistrationForm
from .models import Club, ClubRegistration
from events.models import Event  # make sure this model exists
from user.decorators import user_login_required
from clubs.decorators import club_login_required


# =======================
# Utility Views
# =======================
def club_home(request):
    return HttpResponse("Club app is working!")

# =======================
# Club Registration
# =======================
def club_registration_view(request):
    if request.method == 'POST':
        form = ClubRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Club registration submitted for review.")
            return redirect('clubs:registration_success')
    else:
        form = ClubRegistrationForm()
    return render(request, 'clubs/club_registration_form.html', {'form': form})

def registration_success_view(request):
    return render(request, 'clubs/registration_success.html')

# =======================
# Club Login / Logout
# =======================
from django.contrib.auth.hashers import check_password

def club_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            club = Club.objects.get(username=username)
        except Club.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'clubs/club_login.html')

        if club.check_password(password):
            request.session['club_id'] = club.id
            request.session['club_username'] = club.username
            return redirect('clubs:club_profile')  # redirect to profile
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'clubs/club_login.html')

def club_logout_view(request):
    request.session.flush()
    return redirect('clubs:login')

# =======================
# Club Profile with Tabs
# =======================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from clubs.models import ClubRegistration, Club
from events.models import Event
from django.utils import timezone


def club_profile_tab_view(request, tab):
    # First: check if club is logged in (via session)
    username = request.session.get('club_username')
    club = None
    club_reg = None

    if username:
        try:
            club_reg = ClubRegistration.objects.get(club_username=username)
            if not club_reg.is_approved or not club_reg.approved_club:
                messages.warning(request, "Your club is not approved yet.")
                return render(request, 'clubs/profile.html', {
                    'status': 'pending',
                    'club_registration': club_reg,
                    'active_tab': tab,
                    'events': [],
                    'upcoming_events': [],
                })
            club = club_reg.approved_club
        except ClubRegistration.DoesNotExist:
            messages.error(request, "Club registration not found.")
            return redirect('clubs:register')
    else:
        # fallback for regular logged-in user (accessing via ?club_id=1)
        club_id = request.GET.get('club_id')
        if not club_id:
            messages.error(request, "Invalid or missing club.")
            return redirect('clubs:login')

        club = get_object_or_404(Club, id=club_id, is_active=True)

    # Events
    upcoming_events = Event.objects.filter(club=club, date_time__gte=timezone.now()).order_by('date_time')[:2]
    events = Event.objects.filter(club=club).order_by('date_time') if tab == 'events' else []

    context = {
        'club': club,
        'club_registration': club_reg,
        'active_tab': tab,
        'status': 'approved',
        'upcoming_events': upcoming_events,
        'events': events,
    }

    return render(request, 'clubs/profile.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClubPasswordChangeForm
from .models import Club

from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .forms import ClubPasswordChangeForm, ClubPasswordChangeForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import Club
from .forms import ClubEditForm, ClubPasswordChangeForm

def edit_club_view(request):
    club_id = request.session.get('club_id')
    if not club_id:
        messages.error(request, "You must be logged in as a club to edit.")
        return redirect('clubs:login')

    club = get_object_or_404(Club, id=club_id)

    if request.method == 'POST':
        info_form = ClubEditForm(request.POST, request.FILES, instance=club)
        password_form = ClubPasswordChangeForm(request.POST)

        if 'update_info' in request.POST:
            if info_form.is_valid():
                info_form.save()
                messages.success(request, "Club information updated successfully.")
                return redirect('clubs:club_profile_about')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                if club.check_password(old_password):
                    new_password = password_form.cleaned_data['new_password1']
                    club.password = make_password(new_password)
                    club.save()
                    messages.success(request, "Password changed successfully.")
                    return redirect('clubs:club_profile_about')
                else:
                    messages.error(request, "Current password is incorrect.")
    else:
        info_form = ClubEditForm(instance=club)
        password_form = ClubPasswordChangeForm()

    context = {
        'info_form': info_form,
        'password_form': password_form,
    }
    return render(request, 'clubs/edit_club.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Club
from .forms import MemberForm, ClubMembershipForm

def add_member_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES)
        membership_form = ClubMembershipForm(request.POST)
        if member_form.is_valid() and membership_form.is_valid():
            member = member_form.save()
            membership = membership_form.save(commit=False)
            membership.member = member
            membership.club = club
            membership.save()
            return redirect('clubs:club_profile_members')
    else:
        member_form = MemberForm()
        membership_form = ClubMembershipForm()
    
    return render(request, 'clubs/add_member.html', {
        'member_form': member_form,
        'membership_form': membership_form,
        'club': club
    })


from .models import ClubMembership, Member

def club_profile_members(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    members = ClubMembership.objects.filter(club=club, is_active=True).select_related('member')
    memberships = ClubMembership.objects.filter(club=club).select_related('member')

    # Default: not admin
    is_admin = False

    # If club user is logged in
    club_user_id = request.session.get('club_id')
    if club_user_id:
        # Find if the current user is in this club and has admin role
        try:
            current_member = Member.objects.get(email=request.session.get('club_email'))  # You can also use session['member_id'] if stored
            membership = ClubMembership.objects.get(club=club, member=current_member, is_active=True)
            ADMIN_ROLES = ['president', 'secretary', 'organizing_secretary']
            user_roles = membership.roles.split(',')  # comma separated
            if any(role in ADMIN_ROLES for role in user_roles):
                is_admin = True
        except (Member.DoesNotExist, ClubMembership.DoesNotExist):
            pass

    return render(request, 'clubs/club_members.html', {
        'club': club,
        'members': members,
        'is_admin': is_admin,
        'memberships': memberships,
    })

# clubs/views.py

from django.shortcuts import render, get_object_or_404
from .models import Club

def public_club_profile_view(request, club_id):
    club = get_object_or_404(Club, id=club_id, is_active=True)
    
    return render(request, 'clubs/profile.html', {
        'club': club
    })

from .forms import ClubAdvisorForm


@club_login_required
def add_advisor_view(request):
    if request.method == 'POST':
        form = ClubAdvisorForm(request.POST, request.FILES)
        if form.is_valid():
            advisor = form.save(commit=False)
            advisor.club = request.club
            advisor.save()
            messages.success(request, "Advisor added successfully.")
            return redirect('clubs:club_profile_about')
    else:
        form = ClubAdvisorForm()
    return render(request, 'clubs/add_advisor.html', {'form': form})

@club_login_required
def edit_advisor_view(request, advisor_id):
    advisor = get_object_or_404(ClubAdvisor, id=advisor_id, club=request.club)

    if request.method == 'POST':
        form = ClubAdvisorForm(request.POST, request.FILES, instance=advisor)
        if form.is_valid():
            form.save()
            messages.success(request, "Advisor updated successfully.")
            return redirect('clubs:club_profile_about')
    else:
        form = ClubAdvisorForm(instance=advisor)

    return render(request, 'clubs/edit_advisor.html', {
        'form': form,
        'advisor': advisor,
    })


from django.shortcuts import render, get_object_or_404
from .models import Member, ClubMembership, Club
from .forms import MembershipForm

def member_profile_view(request, club_id, member_id):
    club = get_object_or_404(Club, id=club_id)
    member = get_object_or_404(Member, id=member_id)
    membership = get_object_or_404(ClubMembership, club=club, member=member)

    return render(request, 'clubs/member_profile.html', {
        'club': club,
        'member': member,
        'membership': membership,
    })


from django.views.decorators.http import require_http_methods
from .models import ClubMembership
from .forms import ClubMembershipForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import ClubMembership

def edit_membership_view(request, membership_id):
    membership = get_object_or_404(ClubMembership, id=membership_id)
    club = membership.club
    member = membership.member

    # Your form logic here, e.g.
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return redirect('clubs:member_profile', club.id, member.id)
    else:
        form = MembershipForm(instance=membership)

    return render(request, 'clubs/edit_membership.html', {
        'form': form,
        'club': club,
        'member': member,
    })

@require_http_methods(["POST"])
@club_login_required
def leave_membership_view(request, membership_id):
    membership = get_object_or_404(ClubMembership, id=membership_id, club=request.club)
    membership.is_active = False
    membership.save()
    messages.success(request, 'Member marked as left.')
    return redirect('clubs:club_profile_members', club_id=request.club.id)


def edit_membership_view(request, membership_id):
    membership = ClubMembership.objects.get(id=membership_id)
    member = membership.member

    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES, instance=member)
        membership_form = MembershipForm(request.POST, instance=membership)
        if member_form.is_valid() and membership_form.is_valid():
            member_form.save()
            membership_form.save()
            return redirect('clubs:member_profile', club_id=membership.club.id, member_id=member.id)

    else:
        member_form = MemberForm(instance=member)
        membership_form = MembershipForm(instance=membership)

    context = {
        'member_form': member_form,
        'membership_form': membership_form,
        'membership': membership,
    }
    return render(request, 'clubs/edit_membership.html', context)
