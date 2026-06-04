from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_display = ('name', 'slug', 'product_count')

    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="color:#f97316;font-weight:600">{}</span>', count
        )
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px;border-radius:8px;'
                'border:1px solid #2a2e3d;box-shadow:0 2px 8px rgba(0,0,0,0.2)"/>',
                obj.image.url
            )
        return format_html(
            '<span style="color:#64748b;font-size:0.82rem">No image</span>'
        )
    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'formatted_price', 'stock_status', 'featured_badge', 'is_active')
    list_filter = ('category', 'featured', 'is_active')
    search_fields = ('title', 'summary', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)
    list_per_page = 25

    fieldsets = (
        ('Product Info', {
            'fields': ('category', 'title', 'slug', 'summary', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Seller Details', {
            'fields': ('seller_name', 'external_url'),
            'classes': ('collapse',),
        }),
        ('Catalog Controls', {
            'fields': ('featured', 'is_active')
        }),
    )
    inlines = [ProductImageInline]

    def formatted_price(self, obj):
        return format_html(
            '<span style="color:#22c55e;font-weight:600">₹{}</span>',
            obj.price
        )
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'

    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html(
                '<span style="color:#ef4444;font-weight:600;padding:3px 10px;'
                'background:rgba(239,68,68,0.1);border-radius:20px;font-size:0.78rem">'
                'Out of Stock</span>'
            )
        elif obj.stock <= 5:
            return format_html(
                '<span style="color:#eab308;font-weight:600;padding:3px 10px;'
                'background:rgba(234,179,8,0.1);border-radius:20px;font-size:0.78rem">'
                'Low ({})</span>', obj.stock
            )
        return format_html(
            '<span style="color:#22c55e;font-weight:600;padding:3px 10px;'
            'background:rgba(34,197,94,0.1);border-radius:20px;font-size:0.78rem">'
            '{} in stock</span>', obj.stock
        )
    stock_status.short_description = 'Stock'
    stock_status.admin_order_field = 'stock'

    def featured_badge(self, obj):
        if obj.featured:
            return format_html(
                '<span style="color:#f97316;font-weight:700;padding:3px 10px;'
                'background:rgba(249,115,22,0.12);border-radius:20px;font-size:0.78rem">'
                '⭐ Featured</span>'
            )
        return format_html('<span style="color:#64748b;font-size:0.82rem">—</span>')
    featured_badge.short_description = 'Featured'
    featured_badge.admin_order_field = 'featured'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'star_rating', 'created_at')
    search_fields = ('product__title', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#f97316;font-size:1rem;letter-spacing:2px">{}</span>',
            stars
        )
    star_rating.short_description = 'Rating'
    star_rating.admin_order_field = 'rating'
