from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from DonerBackend import settings

urlpatterns = i18n_patterns(
    path('',include('App.urls.app'),name='App'),
    path('authenticate/', include('Authenticate.urls'), name='Authenticate'),
    path('administrator/', include('App.urls.administrator'), name='Administrator'),
    path('manager/', include('App.urls.manager'), name='Manager'),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    re_path(r'^statics/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
)
