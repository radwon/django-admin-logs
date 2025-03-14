"""
Django Admin Logs - Models.
"""

import django
from django.contrib.admin import models


class LogEntryManager(models.LogEntryManager):
    """The default LogEntry Model Manager."""

    def __init__(self, model=None):
        super().__init__()
        self.model = model
        if django.VERSION >= (5, 1):
            # Prevent RemovedInDjango60Warning by reverting deprecated method
            type(self).log_action = models.LogEntryManager.log_action


class ChangedLogEntryManager(LogEntryManager):
    """A LogEntry Model Manager that ignores logs with no changes."""

    # Deprecated in Django 5.1 to be removed in Django 6.0
    def log_action(
        self,
        user_id,
        content_type_id,
        object_id,
        object_repr,
        action_flag,
        change_message="",
    ):  # pragma: no cover
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

    def log_actions(
        self, user_id, queryset, action_flag, change_message="", single_object=False
    ):
        # Check whether this is a log with no changes that should be ignored
        if action_flag == models.CHANGE and not change_message:
            return None
        else:  # Log as normal
            if django.VERSION < (5, 1, 7):
                return super().log_actions(
                    user_id,
                    queryset,
                    action_flag,
                    change_message,
                    single_object=single_object,
                )
            else:
                return super().log_actions(
                    user_id,
                    queryset,
                    action_flag,
                    change_message,
                )


class NoLogEntryManager(LogEntryManager):
    """A No LogEntry Model Manager."""

    # Deprecated in Django 5.1 to be removed in Django 6.0
    def log_action(self, *args, **kwargs):  # pragma: no cover
        return None

    def log_actions(self, *args, **kwargs):
        # No logging
        if django.VERSION < (5, 1, 7):
            kwargs.pop('single_object', None)
        return None

    def get_queryset(self):
        # No queries
        return super().get_queryset().none()
