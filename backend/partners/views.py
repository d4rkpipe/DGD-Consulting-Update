from rest_framework import generics
from .models import Partner
from .serializers import PartnerSerializer


class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    pagination_class = None
