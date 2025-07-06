from posts.models import Post
from user.models import User

def user_post_count(request):
    if not request.session.get('user_id'):
        return {}

    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {}

    count = Post.objects.filter(user=user).count()

    return {
        'user_post_count': count
    }
