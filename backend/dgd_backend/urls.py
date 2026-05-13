from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),   # for Jazzmin language switcher

    # API
    # Note: 'api/' prefix is added by cPanel Passenger BaseURI in production.
    # In local dev, set API_BASE in frontend to http://localhost:8002 (no /api).
    path('services/', include('services.urls')),
    path('blog/',     include('blog.urls')),
    path('contact/',  include('contacts.urls')),
    path('partners/', include('partners.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel sarlavhalari (o'zbek tilida)
admin.site.site_header = 'DGD Consulting — Admin'
admin.site.site_title  = 'DGD Consulting'
admin.site.index_title = 'Boshqaruv paneli'
