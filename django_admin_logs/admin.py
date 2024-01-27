"""
Django Admin Logs - Model Admin.
"""

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .settings import DJANGO_ADMIN_LOGS_DELETABLE, DJANGO_ADMIN_LOGS_ENABLED


class LogEntryAdmin(admin.ModelAdmin):
    """Log Entry admin interface."""

    date_hierarchy = "action_time"
    fields = (
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    )
    list_display = (
        "action_time",
        "user_link",
        "action_message",
        "content_type",
        "object_link",
    )
    list_filter = (
        "action_flag",
        ("content_type", admin.RelatedOnlyFieldListFilter),
        ("user", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        "object_repr",
        "change_message",
    )

    @admin.display(description="user")
    def user_link(self, obj):
        """Returns the admin change link to the user object."""
        admin_url = reverse(
            f"admin:{obj.user._meta.app_label}_{obj.user._meta.model_name}_change",
            args=[obj.user.pk],
        )
        return format_html('<a href="{}">{}</a>', admin_url, obj.user)

    @admin.display(description="object")
    def object_link(self, obj):
        """Returns the admin link to the log entry object if it exists."""
        admin_url = None if obj.is_deletion() else obj.get_admin_url()
        if admin_url:
            return format_html('<a href="{}">{}</a>', admin_url, obj.object_repr)
        else:
            return obj.object_repr

    @admin.display(description="action")
    def action_message(self, obj):
        """
        Returns the action message.
        Note: this handles deletions which don't return a change message.
        """
        change_message = obj.get_change_message()
        # If there is no change message then use the action flag label
        if not change_message:
            change_message = f"{obj.get_action_flag_display()}."
        return change_message

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("content_type")

    def has_add_permission(self, request):
        """Log entries cannot be added manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Log entries cannot be changed."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Log entries can only be deleted when the setting is enabled."""
        return DJANGO_ADMIN_LOGS_DELETABLE and super().has_delete_permission(
            request, obj
        )

    # Prevent changes to log entries creating their own log entries!
    def log_addition(self, request, obj, message):
        pass

    def log_change(self, request, obj, message):
        pass

    def log_deletion(self, request, obj, object_repr):
        pass


# Register the LogEntry admin if enabled
if DJANGO_ADMIN_LOGS_ENABLED:
    admin.site.register(LogEntry, LogEntryAdmin)
