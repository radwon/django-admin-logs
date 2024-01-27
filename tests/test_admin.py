"""
Django Admin Logs - Test Admin.
"""

from unittest import mock

from django.contrib.admin.models import ADDITION, DELETION, LogEntry
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase
from django.urls import reverse

from django_admin_logs.admin import LogEntryAdmin

User = get_user_model()


class LogEntryAdminTest(TestCase):
    """Tests the LogEntry Model Admin."""

    @classmethod
    def setUpClass(cls):
        """Set up once for all tests."""
        super().setUpClass()
        cls.logentry_admin = LogEntryAdmin(LogEntry, AdminSite())
        cls.admin_user = User.objects.create_superuser(
            "admin",
            "admin@localhost",
            "password",
        )
        cls.staff_user = User.objects.create_user(
            "staff",
            "staff@localhost",
            "password",
            is_staff=True,
        )

    def setUp(self):
        """Set up before each test."""
        self.request = RequestFactory().get("/admin/")

    def test_user_link(self):
        """Test the admin change link to the user object."""
        log_entry = LogEntry(
            user=self.admin_user,
            action_flag=ADDITION,
            content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=self.admin_user.id,
            object_repr=str(self.admin_user),
        )
        admin_url = reverse(
            f"admin:{User._meta.app_label}_{User._meta.model_name}_change",
            args=[log_entry.user.pk],
        )
        self.assertEqual(
            self.logentry_admin.user_link(log_entry),
            f'<a href="{admin_url}">{log_entry.user}</a>',
        )

    def test_object_link(self):
        """Test the admin link to the log entry object."""
        log_entry = LogEntry(
            user=self.admin_user,
            action_flag=ADDITION,
            content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=self.admin_user.id,
            object_repr=str(self.admin_user),
        )
        self.assertEqual(
            self.logentry_admin.object_link(log_entry),
            f'<a href="{log_entry.get_admin_url()}">{log_entry.object_repr}</a>',
        )
        # Test that a DELETION log entry returns object without a link
        log_entry.action_flag = DELETION
        self.assertEqual(
            self.logentry_admin.object_link(log_entry), log_entry.object_repr
        )

    def test_action_message(self):
        """Test getting the action message."""
        log_entry = LogEntry(
            user=self.admin_user,
            action_flag=ADDITION,
            content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=self.admin_user.id,
            object_repr=str(self.admin_user),
        )
        # Ensure a log entry without a change message uses the action flag label
        self.assertEqual(
            self.logentry_admin.action_message(log_entry),
            f"{log_entry.get_action_flag_display()}.",
        )
        # Ensure a log entry with a change message is used for the action message
        change_message = "This is a change message"
        log_entry.change_message = change_message
        self.assertEqual(self.logentry_admin.action_message(log_entry), change_message)

    def test_has_view_permission(self):
        """Test that only users with permission can view the admin logs."""
        # Super users have all permissions
        self.request.user = self.admin_user
        self.assertTrue(self.logentry_admin.has_view_permission(self.request))
        # Other users don't have view permission unless explicitly granted
        self.request.user = self.staff_user
        self.assertFalse(self.logentry_admin.has_view_permission(self.request))

    def test_has_add_permission(self):
        """Test that users cannot add logs."""
        self.request.user = self.admin_user
        self.assertFalse(self.logentry_admin.has_add_permission(self.request))

    def test_has_change_permission(self):
        """Test that users cannot change logs."""
        self.request.user = self.admin_user
        self.assertFalse(self.logentry_admin.has_change_permission(self.request))

    def test_has_delete_permission(self):
        """Test that logs can only be deleted when the setting is enabled."""
        # With the delete setting disabled super users cannot delete logs
        with mock.patch(
            LogEntryAdmin.__module__ + ".DJANGO_ADMIN_LOGS_DELETABLE", False
        ):
            self.request.user = self.admin_user
            self.assertFalse(self.logentry_admin.has_delete_permission(self.request))
        # With the delete setting enabled super users can delete logs
        with mock.patch(
            LogEntryAdmin.__module__ + ".DJANGO_ADMIN_LOGS_DELETABLE", True
        ):
            self.assertTrue(self.logentry_admin.has_delete_permission(self.request))
            # Ensure other users still can't delete logs without permission
            self.request.user = self.staff_user
            self.assertFalse(self.logentry_admin.has_delete_permission(self.request))

    def test_no_log_actions(self):
        """Test that no actions are created for changes to log entries."""
        # Ensure no actions are created for adding log entries
        self.logentry_admin.log_addition(self.request, self.admin_user, "Added")
        query_count = self.logentry_admin.get_queryset(self.request).count()
        self.assertEqual(query_count, 0)
        # Ensure no actions are created for changing log entries
        self.logentry_admin.log_change(self.request, self.admin_user, "Changed")
        query_count = self.logentry_admin.get_queryset(self.request).count()
        self.assertEqual(query_count, 0)
        # Ensure no actions are created for deleting log entries
        self.logentry_admin.log_deletion(self.request, self.admin_user, "Deleted")
        query_count = self.logentry_admin.get_queryset(self.request).count()
        self.assertEqual(query_count, 0)
