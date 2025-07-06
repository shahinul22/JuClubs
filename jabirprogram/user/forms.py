from django import forms
from .models import User

class UserForm(forms.ModelForm):
    raw_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=False  # set to True during creation if needed
    )

    class Meta:
        model = User
        fields = [
            'user_username',
            'raw_password',
            'full_name',
            'email',
            'student_id',
            'batch',
            'session',
            'phone',
            'department',
            'photo',
            'is_approved',
            'is_active',
            'is_verified',
            'verification_code',
            'code_expires_at',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('raw_password')

        if raw_password:
            user.set_password(raw_password)

        if commit:
            user.save()
        return user
