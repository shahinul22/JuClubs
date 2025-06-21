from django.urls import path
from . import views

app_name = 'events'  # Note: app_name is events, not clubs

urlpatterns = [
    path('club/<int:club_id>/events/', views.club_events_list, name='club_events_list'),
    path('event/<int:event_id>/register/', views.event_registration_view, name='event_registration'),
    path('event/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('club/<int:club_id>/events/create/', views.create_event_view, name='create_event'),  # If create event is here
]
