from django.urls import path
from .views import ContactSubmissionView, NewsletterSubscribeView

urlpatterns = [
    path('',                     ContactSubmissionView.as_view(), name='contact-submit'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
]
