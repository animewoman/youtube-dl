from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('converter/', include('converter.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]