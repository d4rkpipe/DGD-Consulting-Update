from rest_framework import serializers
from .models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'name', 'logo', 'website', 'order']

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get('request')
        url = obj.logo.url
        return request.build_absolute_uri(url) if request else url
