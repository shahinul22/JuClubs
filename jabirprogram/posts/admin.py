from django.contrib import admin
from .models import Post, Like, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('content', 'user__user_username', 'location')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content Preview'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    search_fields = ('user__user_username', 'post__content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'short_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__user_username', 'post__content')

    def short_text(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    short_text.short_description = 'Comment Text'
