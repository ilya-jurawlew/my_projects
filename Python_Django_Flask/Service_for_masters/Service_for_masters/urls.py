import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('/', include('app_users.urls')),
    path('/', include('app_calendar.urls')),

    path('debug/', include(debug_toolbar.urls)),
    path('i18n', include('django.conf.urls.i18n'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
