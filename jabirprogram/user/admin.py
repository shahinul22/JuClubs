from django.contrib import admin
from .models import User
from .forms import UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('user_username', 'email', 'full_name', 'batch', 'session', 'department', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('is_approved', 'is_active', 'batch', 'department')
    search_fields = ('user_username', 'email', 'full_name')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)
