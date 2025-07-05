from .models import Club

def logged_club_context(request):
    club_obj = None
    if request.session.get('club_id'):
        try:
            club_obj = Club.objects.get(id=request.session['club_id'])
        except Club.DoesNotExist:
            pass
    return {
        'logged_club': club_obj
    }


from .models import Club

def club_count(request):
    count = Club.objects.filter(is_active=True).count()
    return {
        'club_count': count
    }

from clubs.models import Member  # or from your correct app if not in clubs

def total_member_count(request):
    count = Member.objects.count()
    return {
        'total_member_count': count
    }

# clubs/context_processors.py

from .models import Club

def featured_clubs(request):
    clubs = Club.objects.filter(is_active=True).order_by('-date_established')[:6]
    return {
        'featured_clubs': clubs
    }


from clubs.models import Club, ClubMembership, ClubRegistration

def club_members_context(request):
    context = {}

    # Check if the club is logged in via session
    username = request.session.get('club_username')
    if username:
        try:
            registration = ClubRegistration.objects.get(club_username=username, is_approved=True)
            club = registration.approved_club
            if club:
                members = ClubMembership.objects.filter(club=club, is_active=True).select_related('member').order_by('member__name')
                context['club_logged_in'] = club
                context['club_members'] = members
        except ClubRegistration.DoesNotExist:
            pass

    return context


