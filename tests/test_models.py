"""
Django Admin Logs - Test Models.
"""

from unittest import mock

from django.apps import apps
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

User = get_user_model()


class LogEntryManagerTest(TestCase):
    """Tests the LogEntry Model Manager."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests."""
        cls.user = User.objects.create_user("user", "user@localhost", "password")
        cls.content_type = ContentType.objects.get_for_model(User)

    @mock.patch("django_admin_logs.settings.DJANGO_ADMIN_LOGS_ENABLED", True)
    def test_log_action(self):
        """Test that a log entry is created when admin logs are enabled."""
        # Re-run the app config ready() method to use the test settings
        apps.get_app_config("django_admin_logs").ready()
        # Ensure there are no log entries yet
        self.assertEqual(LogEntry.objects.count(), 0)
        # Create a log entry when admin logs are enabled
        log_entry = LogEntry.objects.log_action(
            self.user.pk, self.content_type.pk, self.user.pk, repr(self.user), CHANGE
        )
        # Ensure the log entry was created for the action
        self.assertEqual(log_entry, LogEntry.objects.first())
        self.assertEqual(LogEntry.objects.count(), 1)


class ChangedLogEntryManagerTest(TestCase):
    """Tests the LogEntry Model Manager that ignores logs with no changes."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests."""
        cls.user = User.objects.create_user("user", "user@localhost", "password")
        cls.content_type = ContentType.objects.get_for_model(User)

    @mock.patch("django_admin_logs.settings.DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED", True)
    def test_unchanged_log_action(self):
        """Test that logs are ignored if there are no changes."""
        # Re-run the app config ready() method to use the test settings
        apps.get_app_config("django_admin_logs").ready()
        # Ensure there are no log entries yet
        self.assertEqual(LogEntry.objects.count(), 0)
        # Attempt to create a log entry with no changes (in the message)
        log_entry = LogEntry.objects.log_action(
            self.user.pk,
            self.content_type.pk,
            self.user.pk,
            repr(self.user),
            CHANGE,
            "",  # No change message
        )
        # Ensure there was no log entry created for the action
        self.assertEqual(log_entry, None)
        self.assertEqual(LogEntry.objects.count(), 0)
        # Ensure a log entry with a change message is still created
        log_entry = LogEntry.objects.log_action(
            self.user.pk,
            self.content_type.pk,
            self.user.pk,
            repr(self.user),
            CHANGE,
            "Changed user",
        )
        self.assertEqual(log_entry, LogEntry.objects.first())
        self.assertEqual(LogEntry.objects.count(), 1)


class NoLogEntryManagerTest(TestCase):
    """Tests the No LogEntry Model Manager."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests."""
        cls.user = User.objects.create_user("user", "user@localhost", "password")
        cls.content_type = ContentType.objects.get_for_model(User)

    @mock.patch("django_admin_logs.settings.DJANGO_ADMIN_LOGS_ENABLED", False)
    def test_no_log_action(self):
        """Test that a log entry is not created when admin logs are disabled."""
        # Re-run the app config ready() method to use the test settings
        apps.get_app_config("django_admin_logs").ready()
        # Ensure there are no log entries yet
        self.assertEqual(LogEntry.objects.count(), 0)
        # Attempt to create a log entry when admin logs are disabled
        log_entry = LogEntry.objects.log_action(
            self.user.pk, self.content_type.pk, self.user.pk, repr(self.user), CHANGE
        )
        # Ensure there was no log entry created for the action
        self.assertEqual(log_entry, None)
        self.assertEqual(LogEntry.objects.count(), 0)
