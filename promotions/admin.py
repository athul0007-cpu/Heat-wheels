from django.contrib import admin
from .models import Coupon, Promotion


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active')
    search_fields = ('code',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_live', 'launch_date')
    search_fields = ('title',)
    list_filter = ('is_live',)
