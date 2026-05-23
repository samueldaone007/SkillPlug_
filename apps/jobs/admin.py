"""
Admin configuration for the jobs app.
"""

from django.contrib import admin
from .models import Job, Application


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    raw_id_fields = ["student"]
    readonly_fields = ["created_at"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "posted_by",
        "budget_string",
        "status",
        "application_count",
        "created_at",
        "is_active",
    ]
    list_filter = ["status", "is_active", "budget_type", "created_at"]
    search_fields = ["title", "description", "posted_by__username", "posted_by__full_name"]
    raw_id_fields = ["posted_by"]
    filter_horizontal = ["required_skills"]
    inlines = [ApplicationInline]
    date_hierarchy = "created_at"
    actions = ["mark_open", "mark_closed", "mark_completed"]
    
    @admin.action(description="Mark selected jobs as open")
    def mark_open(self, request, queryset):
        updated = queryset.update(status="open")
        self.message_user(request, f"{updated} job(s) marked as open.")
    
    @admin.action(description="Mark selected jobs as closed")
    def mark_closed(self, request, queryset):
        updated = queryset.update(status="closed")
        self.message_user(request, f"{updated} job(s) marked as closed.")
    
    @admin.action(description="Mark selected jobs as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(status="completed")
        self.message_user(request, f"{updated} job(s) marked as completed.")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "job",
        "status",
        "proposed_budget",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = [
        "student__username",
        "student__full_name",
        "job__title",
        "message",
    ]
    raw_id_fields = ["student", "job"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    actions = ["mark_accepted", "mark_rejected", "mark_pending"]
    
    @admin.action(description="Mark selected applications as accepted")
    def mark_accepted(self, request, queryset):
        updated = queryset.update(status="accepted")
        self.message_user(request, f"{updated} application(s) marked as accepted.")
    
    @admin.action(description="Mark selected applications as rejected")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} application(s) marked as rejected.")
    
    @admin.action(description="Mark selected applications as pending")
    def mark_pending(self, request, queryset):
        updated = queryset.update(status="pending")
        self.message_user(request, f"{updated} application(s) marked as pending.")
