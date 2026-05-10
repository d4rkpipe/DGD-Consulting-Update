from rest_framework import generics
from django.utils import translation
from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(generics.ListAPIView):
    """Return top-level (parent=None) active services with their sub_services nested."""
    serializer_class = ServiceSerializer
    pagination_class = None  # show all services on one page

    def get_queryset(self):
        # respect ?lang= query parameter for translated fields
        lang = self.request.query_params.get('lang')
        if lang in dict(translation.get_language_info_list(['uz', 'ru', 'en', 'tr']) if hasattr(translation, 'get_language_info_list') else [('uz','uz'),('ru','ru'),('en','en'),('tr','tr')]):
            translation.activate(lang)
        return Service.objects.filter(parent__isnull=True, is_active=True).prefetch_related('sub_services')


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
