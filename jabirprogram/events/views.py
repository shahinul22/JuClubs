from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm
from clubs.models import Club
from user.decorators import user_login_required
from clubs.decorators import club_login_required


@club_login_required
def club_profile_tab_view(request, tab='about'):
    club = request.club
    return render(request, 'clubs/profile.html', {
        'club': club,
        'active_tab': tab,
    })


@user_login_required
def club_events_list(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    events = Event.objects.filter(club=club).order_by('date_time')
    return render(request, 'events/club_events_list.html', {
        'club': club,
        'events': events,
    })


@club_login_required
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

    return render(request, 'events/create_event.html', {
        'form': form,
        'club': club,
    })

def event_registration_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.visibility != 'public':
        messages.error(request, 'This event is not open to public registration.')
        return redirect('events:club_events_list', club_id=event.club.id)

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

    return render(request, 'events/event_registration.html', {
        'form': form,
        'event': event,
    })



def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.visibility != 'public':
        messages.error(request, 'This event is not available for public viewing.')
        return redirect('events:club_events_list', club_id=event.club.id)

    return render(request, 'events/event_detail.html', {
        'event': event,
    })
