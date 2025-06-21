from django.urls import path
from . import views

from .views import (
    club_registration_view,
    registration_success_view,
    club_login_view,
    club_logout_view,
    club_profile_tab_view,
    edit_club_view,
    add_member_view,
    public_club_profile_view,
)

app_name = 'clubs'

urlpatterns = [
    # Authentication & Registration
    path('register/', club_registration_view, name='register'),
    path('registration-success/', registration_success_view, name='registration_success'),
    path('login/', club_login_view, name='login'),
    path('logout/', club_logout_view, name='club_logout'),

    # Main Profile Page (Default to 'about' tab)
    path("profile/", club_profile_tab_view, {'tab': 'about'}, name="club_profile"),

    # Profile Sub-Tabs (Club admin or via ?club_id for public view)
    path("profile/about/", club_profile_tab_view, {'tab': 'about'}, name='club_profile_about'),
    path("profile/members/", club_profile_tab_view, {'tab': 'members'}, name='club_profile_members'),
    path("profile/events/", club_profile_tab_view, {'tab': 'events'}, name='club_profile_events'),
    path("profile/gallery/", club_profile_tab_view, {'tab': 'gallery'}, name='club_profile_gallery'),
    path("profile/resources/", club_profile_tab_view, {'tab': 'resources'}, name='club_profile_resources'),

    # Edit profile (only for club admins)
    path('profile/edit/', edit_club_view, name='edit_club'),

    # Add new member (admin only)
    path('<int:club_id>/add-member/', add_member_view, name='add_member'),

    # Public view (any logged-in student can see club profile with ID)
    path('public/<int:club_id>/', public_club_profile_view, name='public_club_profile'),
]
