from django.urls import path
from .views import CategoryListView, BlogPostListView, BlogPostDetailView

urlpatterns = [
    path('categories/',        CategoryListView.as_view(),  name='blog-category-list'),
    path('posts/',             BlogPostListView.as_view(),  name='blog-post-list'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
]
