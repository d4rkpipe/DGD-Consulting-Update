from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Service


@admin.register(Service)
class ServiceAdmin(TabbedTranslationAdmin):
    list_display = ('number', 'title', 'parent', 'order', 'is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'parent')
    list_editable = ('order', 'is_featured', 'is_active')
    search_fields = ('number', 'title', 'description')
    autocomplete_fields = ('parent',)
    fieldsets = (
        (None, {
            'fields': ('number', 'parent', 'order', 'is_featured', 'is_active')
        }),
        ('Mazmun', {
            'fields': ('title', 'description', 'icon_svg'),
        }),
    )
