"""
Admin configuration for the reviews app.
"""

from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "reviewer",
        "freelancer",
        "rating",
        "comment_preview",
        "created_at",
    ]
    list_filter = ["rating", "created_at"]
    search_fields = [
        "reviewer__username",
        "reviewer__full_name",
        "freelancer__username",
        "freelancer__full_name",
        "comment",
    ]
    raw_id_fields = ["reviewer", "freelancer"]
    date_hierarchy = "created_at"
    
    def comment_preview(self, obj):
        if len(obj.comment) > 80:
            return f"{obj.comment[:80]}..."
        return obj.comment
    comment_preview.short_description = "Comment"
