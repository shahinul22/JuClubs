from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm
from clubs.models import Club  # To get club info for events

# List events of a club
def club_events_list(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    events = Event.objects.filter(club=club).order_by('date_time')
    context = {
        'club': club,
        'events': events,
    }
    return render(request, 'events/club_events_list.html', context)

# Create event for a club
def create_event_view(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:club_events_list', club_id=club.id)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form, 'club': club})

# Register for event
def event_registration_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if registration is open (optional, depends on your logic)
    if not event.is_registration_open():
        messages.error(request, 'Registration for this event is closed.')
        return redirect('events:club_events_list', club_id=event.club.id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            messages.success(request, 'Successfully registered for the event!')
            return redirect('events:club_events_list', club_id=event.club.id)
    else:
        form = EventRegistrationForm()

    return render(request, 'events/event_registration.html', {'form': form, 'event': event})


# events/views.py

from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})
