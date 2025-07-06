from django.contrib import admin
from .models import User
from .forms import UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        'user_username', 'email', 'full_name', 'student_id', 'batch', 'session',
        'department', 'phone', 'is_approved', 'is_active', 'is_verified', 'date_joined'
    )
    list_filter = (
        'is_approved', 'is_active', 'is_verified', 'batch', 'department', 'session'
    )
    search_fields = (
        'user_username', 'email', 'full_name', 'student_id', 'phone'
    )
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {
            'fields': ('user_username', 'raw_password', 'full_name', 'email', 'student_id', 'batch', 'session', 'department', 'phone', 'photo')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_active', 'is_verified')
        }),
        ('Verification', {
            'fields': ('verification_code', 'code_expires_at')
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )

admin.site.register(User, UserAdmin)
