
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.post_list_view, name='list'), 
    path('user/', include('user.urls', namespace='user')),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('posts/', include('posts.urls', namespace='posts')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
