from django.contrib import admin
from .models import Club, Member, ClubMembership, ClubAdvisor, ClubSocialLink, ClubRegistration

# Inline for ClubMembership inside Club admin
class ClubMembershipInline(admin.TabularInline):
    model = ClubMembership
    extra = 1

# Club Admin
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'category', 'date_established', 'is_active')
    search_fields = ('name', 'username', 'category')
    list_filter = ('is_active', 'category')
    inlines = [ClubMembershipInline]

# Member Admin
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'email', 'phone', 'department')
    search_fields = ('name', 'student_id', 'email')
    list_filter = ('department',)

# ClubMembership Admin
@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'club', 'get_roles', 'is_active', 'joined_date', 'leave_date')
    list_filter = ('is_active', 'club')
    search_fields = ('member__name', 'club__name')

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = 'Roles'

# ClubAdvisor Admin
@admin.register(ClubAdvisor)
class ClubAdvisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'club', 'contact', 'email', 'department', 'is_primary')
    list_filter = ('is_primary', 'club')
    search_fields = ('name', 'club__name', 'email')

# ClubSocialLink Admin
@admin.register(ClubSocialLink)
class ClubSocialLinkAdmin(admin.ModelAdmin):
    list_display = ('club', 'facebook', 'instagram', 'linkedin', 'youtube', 'website')
    search_fields = ('club__name',)

# ClubRegistration Admin (Pending registrations)
@admin.register(ClubRegistration)
class ClubRegistrationAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'club_username', 'is_approved', 'submitted_at', 'reviewed_at')
    search_fields = ('club_name', 'club_username')
    list_filter = ('is_approved', 'submitted_at')
    readonly_fields = ('submitted_at', 'reviewed_at')


from django.contrib import admin
from .models import ClubMemberRequest

@admin.register(ClubMemberRequest)
class ClubMemberRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'requested_at', 'is_approved')
    list_filter = ('is_approved', 'requested_at', 'club')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'club__name')
    date_hierarchy = 'requested_at'
    ordering = ('-requested_at',)
