from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from DonerBackend import settings
from administrator.views import LoginView, logout_view

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/',logout_view,name='logout'),
    path('admin/', admin.site.urls),
    path('api/mobile/', include('Api.urls')),
    path('administrator', include('administrator.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    re_path(r'^statics/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
