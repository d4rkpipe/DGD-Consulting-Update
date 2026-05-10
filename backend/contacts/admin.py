from django.contrib import admin
from .models import ContactSubmission, NewsletterSubscriber


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'company', 'service', 'created_at', 'is_processed')
    list_filter = ('service', 'is_processed', 'created_at')
    list_editable = ('is_processed',)
    search_fields = ('name', 'phone', 'company', 'notes')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    list_editable = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    date_hierarchy = 'subscribed_at'
