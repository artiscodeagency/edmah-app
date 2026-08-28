from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'EDMAH — Administration'
admin.site.site_title = 'EDMAH Admin'
admin.site.index_title = 'Tableau de bord'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('accounts.urls')),
    path('', include('admissions.urls')),
    path('', include('communications.urls')),
    path('', include('events.urls')),
    path('', include('certificates.urls')),
    path('', include('learning.urls')),
    path('', include('content.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
