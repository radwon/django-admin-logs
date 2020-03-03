"""
Django Admin Logs - Test Models.
"""
from unittest import mock

from django.apps import apps
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_admin_logs.apps import DjangoAdminLogsConfig

User = get_user_model()


class LogEntryModelTest(TestCase):
    """Tests the LogEntry Model."""

    def create_log_entry(self):
        # Re-run the app config ready() method to use the latest settings
        app_config = apps.get_app_config(DjangoAdminLogsConfig.name)
        app_config.ready()
        # Create a log entry action for a changed user
        user = User.objects.create_user('user', 'user@localhost', 'password')
        content_type_pk = ContentType.objects.get_for_model(User).pk
        log_entry = LogEntry.objects.log_action(
            user.pk, content_type_pk, user.pk, repr(user),
            CHANGE, change_message='Changed user',
        )
        return log_entry

    @mock.patch(DjangoAdminLogsConfig.__module__ + '.DJANGO_ADMIN_LOGS_ENABLED', True)
    def test_log_action(self):
        """Test that a log entry is created when admin logs are enabled."""
        # Ensure there are no log entries yet
        self.assertEqual(LogEntry.objects.count(), 0)
        # Create a log entry when admin logs are enabled
        log_entry = self.create_log_entry()
        # Ensure the log entry was created for the action
        self.assertEqual(log_entry, LogEntry.objects.latest('pk'))
        self.assertEqual(LogEntry.objects.count(), 1)

    @mock.patch(DjangoAdminLogsConfig.__module__ + '.DJANGO_ADMIN_LOGS_ENABLED', False)
    def test_no_log_action(self):
        """Test that a log entry is not created when admin logs are disabled."""
        # Ensure there are no log entries yet
        self.assertEqual(LogEntry.objects.count(), 0)
        # Attempt to create a log entry when admin logs are disabled
        log_entry = self.create_log_entry()
        # Ensure there was no log entry created for the action
        self.assertEqual(log_entry, None)
        self.assertEqual(LogEntry.objects.count(), 0)
