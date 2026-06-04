from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'payment_status', 'coupon_code', 'total_amount', 'placed_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'placed_at')
    search_fields = ('user__username', 'user__email', 'shipping_address', 'billing_address')
    readonly_fields = (
        'user',
        'coupon_code',
        'discount_amount',
        'total_amount',
        'shipping_address',
        'billing_address',
        'notes',
        'placed_at',
    )
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price')
    search_fields = ('order__id', 'product__title')
