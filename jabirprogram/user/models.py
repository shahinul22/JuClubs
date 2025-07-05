from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    user_username = models.CharField(max_length=150, unique=True)
    user_password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=50)
    batch = models.CharField(max_length=10)
    session = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def set_password(self, raw_password):
        self.user_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.user_password)

    def __str__(self):
        return self.user_username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def member_request(self, club):
        """
        Submits a join request to the given club if not already requested.
        Uses lazy loading to avoid circular import.
        """
        from django.apps import apps
        RequestedMember = apps.get_model('clubs', 'RequestedMember')

        if RequestedMember.objects.filter(user=self, club=club, is_approved=False, is_rejected=False).exists():
            return None  # Already requested

        return RequestedMember.objects.create(
            user=self,
            club=club,
            full_name=self.full_name,
            email=self.email,
            student_id=self.student_id,
            phone=self.phone,
            session=self.session,
            department=self.department,
            photo=self.photo,
            batch=self.batch,
        )
        self.reviewed_at = timezone.now()
        self.save()
