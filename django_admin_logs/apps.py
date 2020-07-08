"""
Django Admin Logs - App Config.
"""
from django.apps import AppConfig

from .settings import DJANGO_ADMIN_LOGS_ENABLED


class DjangoAdminLogsConfig(AppConfig):
    name = 'django_admin_logs'
    verbose_name = 'Django Admin Logs'

    def ready(self):
        # Check if admin logs have been disabled
        if DJANGO_ADMIN_LOGS_ENABLED is False:
            from django.contrib.admin.models import LogEntry

            from .models import NoLogEntryManager

            # Change the model manager to one that doesn't log
            LogEntry.objects = NoLogEntryManager(LogEntry)
