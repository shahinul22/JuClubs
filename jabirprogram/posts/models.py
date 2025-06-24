from django.db import models
from django.utils import timezone
from user.models import User  # your custom user model

from django.db import models
from django.utils import timezone
from user.models import User
from clubs.models import Club

# models.py

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_superadmin_post = models.BooleanField(default=False)

    def __str__(self):
        if self.is_superadmin_post:
            author = "Superadmin"
        elif self.user:
            author = self.user.user_username
        elif self.club:
            author = self.club.username
        else:
            author = "Unknown"
        return f"Post by {author} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for Post ID {self.post.id}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user_username} liked Post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.user_username} on Post {self.post.id}"
