from rest_framework import serializers
from .models import Category, BlogPost


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BlogPostListSerializer(serializers.ModelSerializer):
    """For list view — no full content, just excerpt."""
    category = CategorySerializer(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image',
            'category', 'read_time', 'published_at'
        ]

    def get_cover_image(self, obj):
        if not obj.cover_image:
            return None
        request = self.context.get('request')
        url = obj.cover_image.url
        return request.build_absolute_uri(url) if request else url


class BlogPostDetailSerializer(BlogPostListSerializer):
    """Detail view includes full content."""

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ['content']
