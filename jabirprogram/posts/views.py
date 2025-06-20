from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from user.decorators import login_required_custom
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User  # assuming default user model
from user.models import User

def post_list_view(request):
    user_id = request.session.get('user_id')
    current_user = None
    if user_id:
        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            current_user = None

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

from user.models import User

@login_required_custom  # your custom login_required decorator
def create_post(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # Not logged in properly
        return redirect('user:login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user  # Assign custom user instance, not request.user
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required_custom
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

@login_required_custom
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from django.shortcuts import get_object_or_404
from user.models import User  # import your custom User model

@login_required_custom
@require_POST
def toggle_like(request, post_id):
    user = request.user
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


@login_required_custom
@require_POST
def add_comment(request, post_id):
    user = request.user
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


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment

@login_required_custom
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return redirect('home')  # or return 403 Forbidden if you prefer

    if request.method == 'POST':
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))
