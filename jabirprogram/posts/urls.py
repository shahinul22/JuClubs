from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('feed/', views.post_list_view, name='list'),  # We’ll add this next
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/edit/', views.edit_post, name='edit'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
    path('<int:post_id>/like-toggle/', views.toggle_like, name='like_toggle'),
    path('<int:post_id>/comment-add/', views.add_comment, name='comment_add'),
    # urls.py
    # path('post/<int:post_id>/delete/', views.delete_post, name='delete_post')
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment')

]
