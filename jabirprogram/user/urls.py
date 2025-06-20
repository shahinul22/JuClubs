from django.urls import path


app_name = 'user'

from .views import(
    signup_view,
    verify_code_view,
    login_view,
    dashboard_view,
    logout_view,
    profile_view,
    edit_profile_view,
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify/', verify_code_view, name='verify_code'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
]
