from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on delivery'),
        ('card', 'Card payment'),
        ('upi', 'UPI payment'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=24, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=24, choices=PAYMENT_STATUS_CHOICES, default='pending')
    coupon_code = models.CharField(max_length=30, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping_address = models.CharField(max_length=260)
    billing_address = models.CharField(max_length=260)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price
