from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Hamkor'
        verbose_name_plural = 'Hamkorlar'

    def __str__(self):
        return self.name
