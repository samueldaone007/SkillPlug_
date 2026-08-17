"""
Admin configuration for the marketplace app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "image_preview", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title", "description", "user__username", "user__full_name"]
    raw_id_fields = ["user"]
    date_hierarchy = "created_at"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = "Preview"
