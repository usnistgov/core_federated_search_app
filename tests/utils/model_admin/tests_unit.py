""" Unit tests for `utils.model_admin` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from core_federated_search_app.utils import model_admin
from core_federated_search_app.utils.forms import OAuth2ApplicationAdminForm


class TestReadOnlyModelAdmin(TestCase):
    """Unit tests for `ReadOnlyModelAdmin` model."""

    def setUp(self):
        """setUp"""
        self.mock_read_only_model_admin = model_admin.ReadOnlyModelAdmin(
            MagicMock(), MagicMock()
        )

    def test_has_add_permission_false(self):
        """test_has_add_permission_false"""
        self.assertFalse(
            self.mock_read_only_model_admin.has_add_permission(MagicMock())
        )

    def test_has_change_permission_false(self):
        """test_has_change_permission_false"""
        self.assertFalse(
            self.mock_read_only_model_admin.has_change_permission(MagicMock())
        )


class TestOAuth2ApplicationAdmin(TestCase):
    """Unit tests for `OAuth2ApplicationAdmin` model"""

    def test_form_is_oauth2_application_form(self):
        """test_form_is_oauth2_application_form"""
        mock_oauth2_application_admin = model_admin.OAuth2ApplicationAdmin(
            MagicMock(), MagicMock()
        )
        self.assertEqual(
            mock_oauth2_application_admin.form, OAuth2ApplicationAdminForm
        )
