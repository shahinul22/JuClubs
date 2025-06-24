from django import forms
from .models import ClubRegistration

class ClubRegistrationForm(forms.ModelForm):
    club_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ClubRegistration
        exclude = ['is_approved', 'approved_club', 'reviewed_at', 'submitted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            label = field.label if field.label else field_name.replace('_', ' ')

            # Special case for date field
            if field_name == 'date_established':
                placeholder = 'YYYY-MM-DD'
                field.widget.input_type = 'date'  # optional: show date picker
            else:
                placeholder = f'Enter {label.lower()}'

            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded-md py-2 px-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': placeholder
            })


from django import forms
from .models import Club
from django import forms

class ClubEditForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'username', 'category', 'date_established', 'constitution', 'mission_and_vision', 'membership_rules', 'description', 'club_moto', 'logo', 'cover_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add Tailwind CSS classes to every input, select, textarea, and file input
            classes = "w-full border border-gray-300 rounded-md py-2 px-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            if isinstance(field.widget, (forms.FileInput,)):
                classes = "w-full"
            field.widget.attrs.update({'class': classes})


class ClubPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        label="Current Password",
        required=True
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label="New Password",
        required=True
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label="Confirm New Password",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': "w-full border border-gray-300 rounded-md py-2 px-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            })

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The new passwords do not match.")
        
        return cleaned_data
from django import forms
from .models import Member, ClubMembership, ClubAdvisor

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'student_id', 'email', 'phone', 'session', 'department', 'photo']

class ClubMembershipForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=ClubMembership.ROLE_CHOICES,
        widget=forms.SelectMultiple(attrs={
            'class': 'select select-bordered w-full h-40'
        }),
        help_text="Hold Ctrl or Cmd to select multiple roles."
    )

    class Meta:
        model = ClubMembership
        fields = ['roles', 'is_active']

    def clean_roles(self):
        roles = self.cleaned_data['roles']
        return ",".join(roles)  # Store as comma-separated string


from django import forms
from .models import ClubAdvisor

class ClubAdvisorForm(forms.ModelForm):
    class Meta:
        model = ClubAdvisor
        fields = ['name', 'contact', 'email', 'department', 'photo', 'is_primary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'contact': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'department': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'photo': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
        }


class ClubMembershipForm(forms.ModelForm):
    class Meta:
        model = ClubMembership
        fields = ['roles']

from django import forms
from .models import ClubMembership

from django import forms
from .models import ClubMembership

class MembershipForm(forms.ModelForm):
    class Meta:
        model = ClubMembership
        fields = '__all__'  # includes all fields of ClubMembership

from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'  # edit all member fields
