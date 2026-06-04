from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


class Promotion(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    highlight_image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    call_to_action = models.CharField(max_length=80, blank=True)
    is_live = models.BooleanField(default=True)
    launch_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
