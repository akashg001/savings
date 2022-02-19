from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    url(r'^media/(?p<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?p<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),  
]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,documet_root=settings.MEDIA_ROOT)
