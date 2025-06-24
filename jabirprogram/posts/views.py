# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from user.models import User
from clubs.models import Club
from user.decorators import user_login_required
from clubs.decorators import club_login_required
import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

from user.models import User  # your custom User model

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm
from .models import Post, PostImage, User, Club

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm
from .models import Post, PostImage
from user.models import User
from clubs.models import Club

def create_post(request):
    print("🔍 Create post view loaded")

    post_user = None
    post_club = None
    is_superadmin = False

    if request.session.get('user_id'):
        try:
            post_user = User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('user:login')

    elif request.session.get('club_id'):
        try:
            post_club = Club.objects.get(id=request.session['club_id'])
        except Club.DoesNotExist:
            messages.error(request, "Club not found.")
            return redirect('clubs:club_login')

    elif request.user.is_authenticated and request.user.is_superuser:
        is_superadmin = True

    else:
        messages.error(request, "You must be logged in to create a post.")
        return redirect('user:login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = post_user
            post.club = post_club
            post.is_superadmin_post = is_superadmin
            post.save()

            images = request.FILES.getlist('images')
            for img in images:
                PostImage.objects.create(post=post, image=img)

            messages.success(request, "Post created successfully.")
            return redirect('posts:list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})



@user_login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'edit': True})

@user_login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def post_list_view(request):
    user_id = request.session.get('user_id')
    current_user = None
    if user_id:
        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            current_user = None

    # Filters
    filter_type = request.GET.get('filter')
    category = request.GET.get('category')
    date = request.GET.get('date')

    posts = Post.objects.select_related('user', 'club').all()

    if filter_type == 'club':
        posts = posts.filter(club__isnull=False)
    elif filter_type == 'user':
        posts = posts.filter(user__isnull=False)

    if category:
        posts = posts.filter(content__icontains=category)

    if date:
        try:
            target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            posts = posts.filter(created_at__date=target_date)
        except ValueError:
            pass

    posts = posts.order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        return JsonResponse({'html': '', 'has_next': False})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('posts/_post_list.html', {
            'page_obj': page_obj,
            'liked_post_ids': set(),
            'user': current_user,
        }, request=request)
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    liked_post_ids = set()
    if current_user:
        liked_post_ids = set(
            Like.objects.filter(user=current_user, post__in=page_obj.object_list)
            .values_list('post_id', flat=True)
        )

    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'liked_post_ids': liked_post_ids,
        'user': current_user,
    })

@user_login_required
@require_POST
def toggle_like(request, post_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Not authenticated'}, status=403)
    user = User.objects.get(id=user_id)

    post = get_object_or_404(Post, id=post_id)

    liked = Like.objects.filter(post=post, user=user).first()
    if liked:
        liked.delete()
        liked_status = False
    else:
        Like.objects.create(post=post, user=user)
        liked_status = True

    likes_count = post.likes.count()
    return JsonResponse({'liked': liked_status, 'likes_count': likes_count})

@user_login_required
@require_POST
def add_comment(request, post_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=403)
    user = User.objects.get(id=user_id)

    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('text', '').strip()

    if text:
        comment = Comment.objects.create(post=post, user=user, text=text)
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'username': user.user_username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    return JsonResponse({'success': False, 'error': 'Empty comment'})

@user_login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))