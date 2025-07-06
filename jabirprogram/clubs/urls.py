from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    club_registration_view,
    registration_success_view,
    club_login_view,
    club_logout_view,
    club_profile_tab_view,
    edit_club_view,
    add_member_view,
    public_club_profile_view,
    # request_to_join_club,
    # approve_member_request,
    # club_member_requests_view,
    add_advisor_view,
    edit_advisor_view,
)

app_name = 'clubs'

urlpatterns = [
    # Club Auth & Registration
    path('register/', club_registration_view, name='register'),
    path('registration-success/', registration_success_view, name='registration_success'),
    path('login/', club_login_view, name='login'),
    path('logout/', club_logout_view, name='club_logout'),

    # Club Profile (with tab-based routing)
    path("profile/", club_profile_tab_view, {'tab': 'about'}, name="club_profile"),
    path("profile/about/", club_profile_tab_view, {'tab': 'about'}, name='club_profile_about'),
    path("profile/members/", club_profile_tab_view, {'tab': 'members'}, name='club_profile_members'),
    path("profile/events/", club_profile_tab_view, {'tab': 'events'}, name='club_profile_events'),
    path("profile/gallery/", club_profile_tab_view, {'tab': 'gallery'}, name='club_profile_gallery'),
    path("profile/notice/", club_profile_tab_view, {'tab': 'notice'}, name='club_profile_notice'),

    # Profile Edit & Admin Tools
    path('profile/edit/', edit_club_view, name='edit_club'),
    path('<int:club_id>/add-member/', add_member_view, name='add_member'),
    # path("profile/member-requests/", club_member_requests_view, name="club_member_requests"),
    # path('approve-request/<int:request_id>/', approve_member_request, name='approve_member_request'),

    # Public Club View (for users)
    path('public/<int:club_id>/', public_club_profile_view, name='public_club_profile'),
    # path('request-to-join/<int:club_id>/', request_to_join_club, name='request_to_join'),
    # path('request-from-profile/', views.request_to_join_from_profile, name='request_to_join_from_profile'),
    # path('join-request/<int:club_id>/', views.request_to_join_club, name='request_to_join'),
    # path('join-request/<int:club_id>/', views.request_to_join_club, name='request_to_join'),
    # path('approve-member/<int:request_id>/', views.approve_member_request, name='approve_member_request'),
    # clubs/urls.py
    # path('request-to-join/<int:club_id>/', views.request_to_join_club, name='request_to_join'),

    # add advisor
    path('profile/<int:club_id>/add-advisor/', add_advisor_view, name='add_advisor'),

    path('advisor/<int:advisor_id>/edit/', views.edit_advisor_view, name='edit_advisor'),

    # club member profile
    path('profile/member/<int:club_id>/<int:member_id>/', views.member_profile_view, name='member_profile'),
    path('membership/<int:membership_id>/edit/', views.edit_membership_view, name='edit_membership'),
    path('membership/<int:membership_id>/leave/', views.leave_membership_view, name='leave_membership'),


    
    # path('<int:club_id>/join/', views.join_club_view, name='join_club'),
    path('<int:club_id>/join/', views.join_club_view, name='join_club'),
    path('profile/member-requests/', views.club_member_requests_view, name='club_member_requests'),
    path('approve-request/<int:request_id>/', views.approve_member_request, name='approve_request'),
    path('decline-request/<int:request_id>/', views.decline_member_request, name='decline_request'),
    path('request/<int:req_id>/approve/', views.approve_request_view, name='approve_request'),
    path('request/<int:req_id>/decline/', views.decline_request_view, name='decline_request'),
    path("profile/<int:club_id>/", club_profile_tab_view, {'tab': 'about'}, name="club_profile"),

    # clubs/urls.py
    path('<int:club_id>/gallery/upload/', views.club_gallery_upload_view, name='club_gallery_upload'),
    # urls.py
    path('gallery/<int:photo_id>/delete/', views.delete_gallery_photo_view, name='delete_gallery_photo'),

    # path('<int:club_id>/gallery/ajax-upload/', views.ajax_club_gallery_upload, name='ajax_club_gallery_upload'),
    # path('gallery/<int:photo_id>/delete/', views.delete_gallery_photo, name='delete_gallery_photo'),

    # Notice URLs

    path('create-notice/', views.create_club_notice, name='create_club_notice'),

    path('<str:club_username>/notices/', 
         views.ClubNoticeListView.as_view(), 
         name='club_notice_list'),
    
    path('<str:club_username>/notices/create/', 
         views.ClubNoticeCreateView.as_view(), 
         name='club_notice_create'),
    
    path('<str:club_username>/notices/<slug:notice_slug>/', 
         views.ClubNoticeDetailView.as_view(), 
         name='club_notice_detail'),
    
    path('<str:club_username>/notices/<slug:notice_slug>/update/', 
         views.ClubNoticeUpdateView.as_view(), 
         name='club_notice_update'),
    
    path('<str:club_username>/notices/<slug:notice_slug>/delete/', 
         views.ClubNoticeDeleteView.as_view(), 
         name='club_notice_delete'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)