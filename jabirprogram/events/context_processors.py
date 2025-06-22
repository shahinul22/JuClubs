from .models import Event

def total_events_count(request):
    return {
        'total_events': Event.objects.count()
    }


from .models import Event
from django.utils import timezone

def today_events_count(request):
    today = timezone.localdate()
    count = Event.objects.filter(date_time__date=today).count()
    return {
        'today_event_count': count
    }

from .models import Event
from django.utils import timezone
from datetime import timedelta

def current_week_events_count(request):
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    count = Event.objects.filter(date_time__date__range=(start_of_week, end_of_week)).count()

    return {
        'week_event_count': count
    }


from .models import Event
from django.utils import timezone

def current_month_events_count(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)

    count = Event.objects.filter(date_time__date__gte=start_of_month, date_time__date__lt=next_month).count()

    return {
        'month_event_count': count
    }


# yourapp/context_processors.py
from .models import Event
from django.utils import timezone

# yourapp/context_processors.py
from .models import Event
from django.utils import timezone

def upcoming_events_processor(request):
    upcoming_events = Event.objects.filter(
        date_time__gte=timezone.now(),
        visibility='public'  # Only public events
    ).order_by('date_time')[:4]  # get next 4 upcoming events

    return {
        'upcoming_events': upcoming_events,
    }
