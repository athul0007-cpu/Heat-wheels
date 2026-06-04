from django.contrib import admin
from .models import FAQ, SupportMessage


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'featured')
    search_fields = ('question',)


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'email', 'resolved', 'created_at')
    list_filter = ('resolved',)
    search_fields = ('subject', 'message')
