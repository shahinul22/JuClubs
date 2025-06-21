from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import random

from .models import User


def home_view(request):
    return render(request, 'home.html')  # not base.html directly!


def generate_code():
    return str(random.randint(100000, 999999))


def signup_view(request):
    if request.method == 'POST':
        data = request.POST
        required_fields = ['user_username', 'password', 'full_name', 'email', 'batch', 'session', 'department']
        if not all(data.get(field) for field in required_fields):
            messages.error(request, "All fields are required.")
            return render(request, 'user/signup.html')

        if User.objects.filter(user_username=data['user_username']).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'user/signup.html')

        if User.objects.filter(email=data['email']).exists():
            messages.error(request, "Email already used.")
            return render(request, 'user/signup.html')

        code = generate_code()
        expiry = timezone.now() + timezone.timedelta(minutes=10)

        user = User(
            user_username=data['user_username'],
            full_name=data['full_name'],
            email=data['email'],
            batch=data['batch'],
            session=data['session'],
            department=data['department'],
            verification_code=code,
            code_expires_at=expiry
        )
        user.set_password(data['password'])
        user.save()

        send_mail(
            subject="Your JUClubs account verification code",
            message=f"Hi {user.full_name},\n\nYour verification code is: {code}\nIt will expire in 10 minutes.\n\nThank you for joining JUClubs!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        request.session['user_pending_verification'] = user.id
        return redirect('user:verify_code')

    return render(request, 'user/signup.html')


def verify_code_view(request):
    user_id = request.session.get('user_pending_verification')
    if not user_id:
        return redirect('user:signup')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('user:signup')

    if request.method == 'POST':
        input_code = request.POST.get('verification_code')

        if timezone.now() > user.code_expires_at:
            messages.error(request, "Code expired. Please log in again to receive a new one.")
            return redirect('user:login')

        if input_code != user.verification_code:
            messages.error(request, "Invalid code.")
            return render(request, 'user/verify_code.html')

        user.is_verified = True
        user.verification_code = None
        user.code_expires_at = None
        user.save()
        del request.session['user_pending_verification']

        # Send confirmation email after successful verification
        send_mail(
            subject="JUClubs Account Verified",
            message=f"Hi {user.full_name},\n\nYour account has been successfully verified. You can now log in and enjoy all the features of JUClubs!\n\nRegards,\nJUClubs Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        messages.success(request, "Email verified. You can now log in.")
        return redirect('user:login')

    return render(request, 'user/verify_code.html')


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
                message=f"Hello {user.full_name},\n\nYour new verification code is: {code}\nIt will expire in 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

            request.session['user_pending_verification'] = user.id
            messages.warning(request, 'A new verification code has been sent to your email.')
            return redirect('user:verify_code')

        request.session['user_id'] = user.id
        request.session['username'] = user.user_username
        messages.success(request, f'Welcome, {user.full_name}!')
        return redirect('home')

    return render(request, 'user/login.html')


def dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('user:login')
    return render(request, 'user/dashboard.html')


def logout_view(request):
    request.session.flush()
    return redirect('user:login')



def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('user:login')
    return render(request, 'user/profile.html', {'user': user})
def edit_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('user:login')

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.batch = request.POST.get('batch')
        user.session = request.POST.get('session')
        user.department = request.POST.get('department')

        # Handle photo upload
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user:profile')

    return render(request, 'user/edit_profile.html', {'user': user})
