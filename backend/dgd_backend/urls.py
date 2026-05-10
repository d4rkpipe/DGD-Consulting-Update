from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # API
    path('api/services/', include('services.urls')),
    path('api/blog/',     include('blog.urls')),
    path('api/contact/',  include('contacts.urls')),
    path('api/partners/', include('partners.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin panel sarlavhalari (o'zbek tilida)
admin.site.site_header = 'DGD Consulting — Admin'
admin.site.site_title  = 'DGD Consulting'
admin.site.index_title = 'Boshqaruv paneli'
