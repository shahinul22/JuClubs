from django.contrib import admin
from .models import (
    Event,
    EventRegistrationQuestion,
    EventRegistration,
    EventAttendance,
    EventFeedback,
)

class EventRegistrationQuestionInline(admin.TabularInline):
    model = EventRegistrationQuestion
    extra = 1

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1
    readonly_fields = ('registered_at',)

class EventAttendanceInline(admin.TabularInline):
    model = EventAttendance
    readonly_fields = ('check_in_time',)

class EventFeedbackInline(admin.TabularInline):
    model = EventFeedback
    readonly_fields = ('submitted_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date_time', 'location', 'event_type', 'visibility')
    list_filter = ('club', 'event_type', 'visibility', 'date_time')
    search_fields = ('title', 'club__name', 'location', 'organizer_name')

    inlines = [
        EventRegistrationQuestionInline,
        EventRegistrationInline,
        EventAttendanceInline,
        EventFeedbackInline,
    ]

@admin.register(EventRegistrationQuestion)
class EventRegistrationQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'event', 'is_required')
    list_filter = ('event', 'is_required')
    search_fields = ('question_text',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'payment_status', 'confirmed', 'registered_at')
    list_filter = ('event', 'payment_status', 'confirmed')
    search_fields = ('full_name', 'email')

@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ('registration', 'event', 'checked_in', 'check_in_time')
    list_filter = ('checked_in', 'event')
    search_fields = ('registration__full_name',)

@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'rating', 'submitted_at')
    list_filter = ('event', 'rating')
    search_fields = ('comment',)
