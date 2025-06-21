
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from posts import views
from user import views



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home_view, name='home'), 
    path('user/', include('user.urls', namespace='user')),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('events/', include('events.urls', namespace='events')),
    path('clubs/', include('clubs.urls', namespace='clubs')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
