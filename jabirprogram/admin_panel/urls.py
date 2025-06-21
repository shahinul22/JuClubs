from django.urls import path
from .views import (
    admin_login_view,
    admin_logout_view,
    admin_dashboard_view,
    delete_user_view,
    pending_club_list_view,
    approve_club_view,
)

app_name = 'admin_panel'

urlpatterns = [
    path('login/', admin_login_view, name='admin_login_view'),
    path('logout/', admin_logout_view, name='admin_logout_view'),
    path('dashboard/', admin_dashboard_view, name='admin_dashboard_view'),
    path('delete-user/<int:user_id>/', delete_user_view, name='delete_user'),
    path('pending-clubs/', pending_club_list_view, name='pending_list'),
    path('approve-club/<int:reg_id>/', approve_club_view, name='approve_club'),
]
