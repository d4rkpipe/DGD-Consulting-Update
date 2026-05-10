from rest_framework import generics
from django.utils import translation
from .models import Category, BlogPost
from .serializers import (
    CategorySerializer, BlogPostListSerializer, BlogPostDetailSerializer
)


def _activate_lang(request):
    lang = request.query_params.get('lang')
    if lang in ('uz', 'ru', 'en', 'tr'):
        translation.activate(lang)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        _activate_lang(request)
        return super().list(request, *args, **kwargs)


class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        _activate_lang(self.request)
        qs = BlogPost.objects.filter(is_published=True).select_related('category', 'author')
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs


class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        _activate_lang(self.request)
        return BlogPost.objects.filter(is_published=True).select_related('category', 'author')
