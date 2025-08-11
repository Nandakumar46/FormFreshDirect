# farmfreshdirect/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.home, name='home'), # Home page
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)