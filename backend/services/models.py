from django.db import models


class Service(models.Model):
    """A service or sub-service offered by DGD Consulting."""

    number = models.CharField(
        max_length=10,
        help_text="Tartib raqami: '01', '02', '5.1', va h.k."
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_svg = models.TextField(
        blank=True,
        help_text="SVG markup (path d=..., circle, line, va h.k.)"
    )
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='sub_services',
        help_text="Agar bu sub-xizmat bo'lsa, ota xizmatni tanlang"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="'NEW' badge bilan ko'rsatish (masalan AI/ML uchun)"
    )
    order = models.PositiveIntegerField(default=0, help_text="Saralash tartibi")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'number']
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'

    def __str__(self):
        return f"{self.number} · {self.title}"

    @property
    def has_sub_services(self):
        return self.sub_services.exists()
