from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import FileResponse, Http404
import os
from core.views import health_check


def serve_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.isfile(file_path):
        return FileResponse(open(file_path, 'rb'))
    raise Http404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
]

if not os.environ.get('CLOUDINARY_URL'):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]
