from django.urls import path
from .views import (
    signup_view,
    verify_code_view,
    login_view,
    dashboard_view,
    logout_view,
    profile_view,
    edit_profile_view,
)

app_name = 'user'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify/', verify_code_view, name='verify_code'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    # Logged-in user's profile
    path('profile/', profile_view, name='profile'),

    # Any user's profile by user_id
    path('profile/<int:user_id>/', profile_view, name='profile_with_id'),

    path('profile/edit/', edit_profile_view, name='edit_profile'),
]
