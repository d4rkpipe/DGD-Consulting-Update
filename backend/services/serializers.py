from rest_framework import serializers
from .models import Service


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'number', 'title', 'description', 'icon_svg', 'is_featured', 'order']


class ServiceSerializer(serializers.ModelSerializer):
    sub_services = SubServiceSerializer(many=True, read_only=True)
    stages = serializers.SerializerMethodField()

    def get_stages(self, obj):
        if not obj.stages:
            return []
        return [s.strip() for s in obj.stages.split(',') if s.strip()]

    class Meta:
        model = Service
        fields = [
            'id', 'number', 'title', 'description', 'outcome',
            'icon_svg', 'stages', 'is_featured', 'order', 'sub_services'
        ]
