from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date_time', 'end_time', 'location',
            'poster', 'organizer_name', 'organizer_contact', 'capacity',
            'visibility', 'event_type', 'registration_deadline',
            'is_paid', 'ticket_price',
        ]
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_paid = cleaned_data.get('is_paid')
        ticket_price = cleaned_data.get('ticket_price')

        if is_paid and (ticket_price is None or ticket_price <= 0):
            self.add_error('ticket_price', 'Ticket price must be positive for paid events.')
        return cleaned_data



from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['full_name', 'email', 'phone', 'affiliation', 'custom_answers']
        widgets = {
            'custom_answers': forms.Textarea(attrs={'rows': 3}),
        }
