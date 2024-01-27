"""
Django Admin Logs - Models.
"""

from django.contrib.admin import models


class LogEntryManager(models.LogEntryManager):
    """The default LogEntry Model Manager."""

    def __init__(self, model=None):
        super().__init__()
        self.model = model


class ChangedLogEntryManager(LogEntryManager):
    """A LogEntry Model Manager that ignores logs with no changes."""

    def log_action(
        self,
        user_id,
        content_type_id,
        object_id,
        object_repr,
        action_flag,
        change_message="",
    ):
        # Check whether this is a log with no changes that should be ignored
        if action_flag == models.CHANGE and not change_message:
            return None
        else:  # Log as normal
            return super().log_action(
                user_id,
                content_type_id,
                object_id,
                object_repr,
                action_flag,
                change_message,
            )


class NoLogEntryManager(LogEntryManager):
    """A No LogEntry Model Manager."""

    def log_action(self, *args, **kwargs):
        # No logging
        return None

    def get_queryset(self):
        # No queries
        return super().get_queryset().none()
