from django.contrib import admin
from .models import SiteBanner


@admin.register(SiteBanner)
class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    search_fields = ('title', 'subtitle')
    list_filter = ('is_active',)
