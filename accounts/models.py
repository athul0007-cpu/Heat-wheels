from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Stores extra profile details for each customer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=24, blank=True)
    city = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=260, blank=True)
    pincode = models.CharField(max_length=12, blank=True)
    favorite_collection = models.CharField(max_length=120, blank=True)
    wishlist = models.ManyToManyField('products.Product', blank=True, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
