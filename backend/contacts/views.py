from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission, NewsletterSubscriber
from .serializers import ContactSubmissionSerializer, NewsletterSubscriberSerializer


class ContactSubmissionView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

    def perform_create(self, serializer):
        submission = serializer.save()
        # Notify admin via email
        try:
            send_mail(
                subject=f"DGD Consulting — Yangi so'rov: {submission.name}",
                message=(
                    f"Ism: {submission.name}\n"
                    f"Kompaniya: {submission.company or '-'}\n"
                    f"Telefon: {submission.phone}\n"
                    f"Xizmat: {submission.get_service_display()}\n\n"
                    f"Izoh:\n{submission.notes or '-'}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            # Don't fail the request if email fails
            pass


class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # idempotent — re-subscribe if previously inactive
        obj, created = NewsletterSubscriber.objects.update_or_create(
            email=email, defaults={'is_active': True}
        )
        return Response(
            {'email': obj.email, 'created': created},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
