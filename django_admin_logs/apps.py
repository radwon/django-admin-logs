"""
Django Admin Logs - App Config.
"""

from django.apps import AppConfig


class DjangoAdminLogsConfig(AppConfig):
    name = "django_admin_logs"
    verbose_name = "Django Admin Logs"

    def ready(self):
        # Import models after apps loaded to avoid AppRegistryNotReady exception
        from django.contrib.admin.models import LogEntry

        from .models import ChangedLogEntryManager, LogEntryManager, NoLogEntryManager
        from .settings import (
            DJANGO_ADMIN_LOGS_ENABLED,
            DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED,
        )

        # Check which LogEntry model manager to use based on settings
        if DJANGO_ADMIN_LOGS_ENABLED is False:
            # Switch to the model manager that doesn't log
            LogEntry.objects = NoLogEntryManager(LogEntry)
        elif DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED is True:
            # Switch to the model manager that only logs changes
            LogEntry.objects = ChangedLogEntryManager(LogEntry)
        else:  # Use the default model manager
            LogEntry.objects = LogEntryManager(LogEntry)
