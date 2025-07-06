from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import random

from .models import User
from clubs.models import Club

# Utility function
def generate_code():
    return str(random.randint(100000, 999999))

# Home view
def home_view(request):
    return render(request, 'home.html')

# Sign-up view
def signup_view(request):
    if request.method == 'POST':
        data = request.POST
        required_fields = [
            'user_username', 'password', 'full_name', 'email',
            'student_id', 'phone', 'batch', 'session', 'department'
        ]

        if not all(data.get(field) for field in required_fields):
            messages.error(request, "All fields are required.")
            return render(request, 'user/signup.html')

        email = data['email'].strip()
        if not email.endswith('@juniv.edu'):
            messages.error(request, "Only JU students can register using a valid @juniv.edu email.")
            return render(request, 'user/signup.html')

        if User.objects.filter(user_username=data['user_username']).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'user/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used.")
            return render(request, 'user/signup.html')

        code = generate_code()
        expiry = timezone.now() + timezone.timedelta(minutes=10)

        user = User(
            user_username=data['user_username'],
            full_name=data['full_name'],
            email=email,
            student_id=data['student_id'],
            phone=data['phone'],
            batch=data['batch'],
            session=data['session'],
            department=data['department'],
            verification_code=code,
            code_expires_at=expiry,
            is_verified=False
        )
        user.set_password(data['password'])
        user.save()

        send_mail(
            subject="Your JUClubs account verification code",
            message=f"Hi {user.full_name},\n\nYour verification code is: {code}\nIt will expire in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        request.session['user_pending_verification'] = user.id
        return redirect('user:verify_code')

    return render(request, 'user/signup.html')

# Verification view
def verify_code_view(request):
    user_id = request.session.get('user_pending_verification')
    if not user_id:
        return redirect('user:signup')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        input_code = request.POST.get('verification_code', '').strip()

        if not user.code_expires_at or timezone.now() > user.code_expires_at:
            messages.error(request, "Verification code has expired. Please request a new one.")
            return redirect('user:login')

        if input_code != user.verification_code:
            messages.error(request, "Invalid verification code. Please try again.")
            return render(request, 'user/verify_code.html')

        user.is_verified = True
        user.verification_code = None
        user.code_expires_at = None
        user.save()

        request.session.pop('user_pending_verification', None)

        send_mail(
            subject="JUClubs Account Verified",
            message=(
                f"Hi {user.full_name},\n\nYour account has been verified. You can now log in.\n\nRegards,\nJUClubs Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        messages.success(request, "Email verified. Please log in.")
        return redirect('user:login')

    return render(request, 'user/verify_code.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('user:login')

        if not user.check_password(password):
            messages.error(request, 'Incorrect password')
            return redirect('user:login')

        if not user.is_verified:
            code = generate_code()
            user.verification_code = code
            user.code_expires_at = timezone.now() + timezone.timedelta(minutes=10)
            user.save()

            send_mail(
                subject="JUClubs Verification Code",
                message=f"Hello {user.full_name},\n\nYour verification code is: {code}\nIt expires in 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

            request.session['user_pending_verification'] = user.id
            messages.warning(request, 'Verification code sent to your email.')
            return redirect('user:verify_code')

        request.session['user_id'] = user.id
        request.session['username'] = user.user_username
        messages.success(request, f'Welcome, {user.full_name}!')
        return redirect('home')

    return render(request, 'user/login.html')

# Dashboard view
def dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('user:login')
    return render(request, 'user/dashboard.html')

# Logout view
def logout_view(request):
    request.session.flush()
    return redirect('user:login')

# Profile view
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User

from posts.models import Post  # import your Post model

from posts.models import Post  # adjust if your Post model is in a different app
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
from user.models import User

def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        if not request.user.is_authenticated:
            return redirect('user:login')
        profile_user = request.user

    post_count = Post.objects.filter(user=profile_user).count()

    return render(request, 'user/profile.html', {
        'profile_user': profile_user,
        'post_count': post_count,
    })

# Edit Profile view
def edit_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.batch = request.POST.get('batch')
        user.session = request.POST.get('session')
        user.department = request.POST.get('department')
        user.phone = request.POST.get('phone')
        user.student_id = request.POST.get('student_id')

        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user:profile')

    return render(request, 'user/edit_profile.html', {'user': user})

# Optional extra profile with club list
def user_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')
    user = get_object_or_404(User, id=user_id)
    clubs = Club.objects.filter(is_active=True)
    return render(request, 'user/profile.html', {'user': user, 'clubs': clubs})
