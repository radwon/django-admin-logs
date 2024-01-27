"""
Django Admin Logs - Settings.
"""

from django.conf import settings

# Determines whether admin logs should be enabled (defaults to True).
# If disabled, no log entries are created or displayed in the admin section.
DJANGO_ADMIN_LOGS_ENABLED = getattr(settings, "DJANGO_ADMIN_LOGS_ENABLED", True)

# Determines whether admin logs are deletable (defaults to False).
# If enabled, non supers users will still require the delete_logentry permission.
DJANGO_ADMIN_LOGS_DELETABLE = getattr(settings, "DJANGO_ADMIN_LOGS_DELETABLE", False)

# Determines whether to ignore (not log) CHANGE actions where no changes were made
# (defaults to False).
DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED = getattr(
    settings, "DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED", False
)
