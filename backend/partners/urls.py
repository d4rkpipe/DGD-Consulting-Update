from django.urls import path
from .views import PartnerListView

urlpatterns = [
    path('', PartnerListView.as_view(), name='partner-list'),
]
