from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category, BlogPost


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'category', 'author', 'read_time', 'is_published', 'published_at')
    list_filter = ('is_published', 'category', 'author', 'published_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('category', 'author')
    date_hierarchy = 'published_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'author', 'cover_image')
        }),
        ('Mazmun', {
            'fields': ('excerpt', 'content'),
        }),
        ('Sozlamalar', {
            'fields': ('read_time', 'is_published', 'published_at'),
        }),
    )
