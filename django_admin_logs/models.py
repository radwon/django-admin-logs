"""
Django Admin Logs - Models.
"""
from django.contrib.admin.models import LogEntryManager


class NoLogEntryManager(LogEntryManager):
    """The No LogEntry Model Manager."""

    def __init__(self, model=None):
        super().__init__()
        self.model = model

    def log_action(self, *args, **kwargs):
        # No logging
        return None

    def get_queryset(self):
        # No queries
        return super().get_queryset().none()
