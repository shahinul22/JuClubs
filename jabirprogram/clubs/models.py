from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


# === Approved Clubs ===
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    category = models.CharField(max_length=255)
    date_established = models.DateField()
    constitution = models.TextField(blank=True)
    mission_and_vision = models.TextField(blank=True)
    membership_rules = models.TextField(blank=True)
    description = models.TextField(blank=True)
    club_moto = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='club_covers/', blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name



# === Master Member Table ===
class Member(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    session = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=255, default='Not Specified')
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)

    class Meta:
        unique_together = ('student_id', 'email')

    def __str__(self):
        return f"{self.name} ({self.student_id})"




# === Club Member Roles ===
class ClubMembership(models.Model):
    ROLE_CHOICES = (
        # Core Executive Team
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('joint_secretary', 'Joint Secretary'),
        ('assistant_secretary', 'Assistant Secretary'),
        ('organizing_secretary', 'Organizing Secretary'),    
        ('treasurer', 'Treasurer'),
        ('financial_controller', 'Financial Controller'),

        # Operational Roles
        ('event_manager', 'Event Manager'),
        ('event_coordinator', 'Event Coordinator'),
        ('logistics_head', 'Logistics Head'),
        ('operations_manager', 'Operations Manager'),

        # Communications
        ('pr_officer', 'Public Relations Officer'),
        ('communications_officer', 'Communications Officer'),
        ('media_coordinator', 'Media Coordinator'),
        ('social_media_manager', 'Social Media Manager'),

        # Creative & Technical
        ('creative_director', 'Creative Director'),
        ('design_head', 'Design Head'),
        ('technical_head', 'Technical Head'),
        ('content_creator', 'Content Creator'),
        ('graphic_designer', 'Graphic Designer'),
        ('webmaster', 'Webmaster'),
        ('photographer', 'Photographer'),
        ('videographer', 'Videographer'),

        # Membership & Outreach
        ('membership_coordinator', 'Membership Coordinator'),
        ('outreach_coordinator', 'Outreach Coordinator'),
        ('partnership_coordinator', 'Partnership Coordinator'),
        ('fundraising_officer', 'Fundraising Officer'),
        ('alumni_relations', 'Alumni Relations Officer'),

        # Specialized Departments
        ('cultural_secretary', 'Cultural Secretary'),
        ('sports_secretary', 'Sports Secretary'),
        ('academic_head', 'Academic Head'),
        ('research_head', 'Research Head'),
        ('training_head', 'Training Head'),
        ('welfare_officer', 'Welfare Officer'),
        ('equity_officer', 'Equity Officer'),

        # Advisory & Support
        ('faculty_advisor', 'Faculty Advisor'),
        ('mentor', 'Mentor'),
        ('legal_advisor', 'Legal Advisor'),
        ('auditor', 'Auditor'),

        # General Roles
        ('project_manager', 'Project Manager'),
        ('volunteer_coordinator', 'Volunteer Coordinator'),
        ('general_member', 'General Member'),
        ('executive_member', 'Executive Member'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    roles = models.CharField(max_length=255)  # Comma-separated string for roles
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(default=timezone.now)
    leave_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('member', 'club')

    def save(self, *args, **kwargs):
        if not self.is_active and self.leave_date is None:
            self.leave_date = timezone.now().date()
        elif self.is_active:
            self.leave_date = None
        super().save(*args, **kwargs)

    def get_roles_display(self):
        return ", ".join(self.roles.split(','))

    def get_roles_list(self):
        return [role.strip() for role in self.roles.split(',') if role.strip()]
        
    def __str__(self):
        return f"{self.member.name} in {self.club.name} as {self.get_roles_display()}"


# === Club Advisor ===
class ClubAdvisor(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='advisors')
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='advisor_photos/', blank=True, null=True)  # 👈 add this line

    def __str__(self):
        return f"{self.name} (Advisor - {self.club.name})"


# === Social Links ===
class ClubSocialLink(models.Model):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name='social_links')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"Social links for {self.club.name}"


# === Pending Registration ===
class ClubRegistration(models.Model):
    club_username = models.CharField(max_length=150, unique=True)
    club_password = models.CharField(max_length=128)

    club_name = models.CharField(max_length=255)
    club_category = models.CharField(max_length=255)
    date_established = models.DateField()
    club_moto = models.CharField(max_length=255, blank=True)

    president_name = models.CharField(max_length=255)
    president_student_id = models.CharField(max_length=50)
    president_email = models.EmailField()
    president_phone = models.CharField(max_length=20)
    president_session = models.CharField(max_length=20)
    president_department = models.CharField(max_length=255)

    secretary_name = models.CharField(max_length=255)
    secretary_student_id = models.CharField(max_length=50)
    secretary_email = models.EmailField()
    secretary_phone = models.CharField(max_length=20)
    secretary_session = models.CharField(max_length=20)
    secretary_department = models.CharField(max_length=255)

    organizing_secretary_name = models.CharField(max_length=255)
    organizing_secretary_student_id = models.CharField(max_length=50)
    organizing_secretary_email = models.EmailField()
    organizing_secretary_phone = models.CharField(max_length=20)
    organizing_secretary_session = models.CharField(max_length=20)
    organizing_secretary_department = models.CharField(max_length=255)

    other_executive_members = models.TextField(blank=True)
    club_constitution = models.TextField(blank=True)
    mission_and_vision = models.TextField(blank=True)
    membership_rules = models.TextField(blank=True)

    advisor_name = models.CharField(max_length=255, blank=True)
    advisor_contact = models.CharField(max_length=255, blank=True)
    advisor_email = models.EmailField(blank=True, default='')
    advisor_department = models.CharField(max_length=255, blank=True, default='')

    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    is_approved = models.BooleanField(default=False)
    approved_club = models.OneToOneField('Club', null=True, blank=True, on_delete=models.SET_NULL)

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.club_password.startswith('pbkdf2_'):
            self.club_password = make_password(self.club_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.club_name} ({'Approved' if self.is_approved else 'Pending'})"

    def approve(self):
        if self.is_approved:
            return  # Skip if already approved

        club = Club.objects.create(
            name=self.club_name,
            username=self.club_username,
            password=self.club_password,
            category=self.club_category,
            date_established=self.date_established,
            constitution=self.club_constitution,
            mission_and_vision=self.mission_and_vision,
            membership_rules=self.membership_rules,
            description=self.other_executive_members,
            club_moto=self.club_moto,
            is_active=True
        )

        # Add or get unique member and assign membership
        def create_member(name, sid, email, phone, session, dept, role):
            member, _ = Member.objects.get_or_create(
                student_id=sid,
                defaults={'name': name, 'email': email, 'phone': phone, 'session': session, 'department': dept}
            )
            ClubMembership.objects.get_or_create(
                member=member, club=club,
                defaults={'roles': role}
            )

        create_member(self.president_name, self.president_student_id, self.president_email, self.president_phone, self.president_session, self.president_department, 'president')
        create_member(self.secretary_name, self.secretary_student_id, self.secretary_email, self.secretary_phone, self.secretary_session, self.secretary_department, 'secretary')
        create_member(self.organizing_secretary_name, self.organizing_secretary_student_id, self.organizing_secretary_email, self.organizing_secretary_phone, self.organizing_secretary_session, self.organizing_secretary_department, 'organizing_secretary')

        if self.advisor_name:
            ClubAdvisor.objects.create(
                club=club,
                name=self.advisor_name,
                contact=self.advisor_contact,
                email=self.advisor_email,
                department=self.advisor_department
            )

        ClubSocialLink.objects.create(
            club=club,
            facebook=self.facebook_link,
            instagram=self.instagram_link,
            linkedin=self.linkedin_link,
            youtube=self.youtube_link,
            website=self.website_link
        )

        self.is_approved = True
        self.approved_club = club
        self.reviewed_at = timezone.now()
        self.save()




from django.db import models
from user.models import User
from clubs.models import Club

class ClubMemberRequest(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='member_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} -> {self.club.name}"
