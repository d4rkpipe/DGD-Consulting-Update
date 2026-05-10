from django.db import models


SERVICE_CHOICES = [
    ('geological_consulting',  'Geologik konsalting'),
    ('comprehensive_project',  'Kompleks loyiha tayyorlash'),
    ('exploration_works',      'Geologik tadqiqot ishlari'),
    ('mre_report',             'MRE hisobot tayyorlash'),
    ('geochemical_research',   'Geokimyoviy tadqiqot'),
    ('geophysical_research',   'Geofizik tadqiqot'),
    ('structural_studies',     'Maxsus strukturaviy tadqiqotlar'),
    ('satellite_processing',   "Sun'iy yo'ldosh tasvirini qayta ishlash"),
    ('ai_ml_prediction',       'AI / ML kon bashorati'),
    ('qaqc_crm',               "QA/QC va CRM qo'llab-quvvatlash"),
    ('other',                  'Boshqa / hali aniq emas'),
]


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30)
    service = models.CharField(
        max_length=40, choices=SERVICE_CHOICES, default='other'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(
        default=False,
        help_text="Admin javob berdi yoki yo'q"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bog'lanish so'rovi"
        verbose_name_plural = "Bog'lanish so'rovlari"

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.get_service_display()}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter obunachi'
        verbose_name_plural = 'Newsletter obunachilari'

    def __str__(self):
        return self.email
