from rest_framework import serializers
from .models import Service


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'number', 'title', 'description', 'icon_svg', 'is_featured', 'order']


class ServiceSerializer(serializers.ModelSerializer):
    sub_services = SubServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'number', 'title', 'description', 'icon_svg',
            'is_featured', 'order', 'sub_services'
        ]
