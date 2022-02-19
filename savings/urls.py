from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.static import serve
from django.urls import re_path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    re_path(r'^media/(?p<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?p<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),  
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT )