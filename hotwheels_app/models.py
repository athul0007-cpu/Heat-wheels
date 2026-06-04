from django.db import models


class SiteBanner(models.Model):
    """Promotional banners displayed on the homepage and campaign pages."""
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=240, blank=True)
    background_image = models.ImageField(upload_to='banners/', blank=True, null=True)
    cta_text = models.CharField(max_length=64, blank=True)
    cta_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Site Banner'
        verbose_name_plural = 'Site Banners'

    def __str__(self):
        return self.title
