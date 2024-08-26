""" Unit tests for `utils.forms` package.
"""

from unittest import TestCase
from unittest.mock import patch

from core_federated_search_app.utils import forms as utils_forms


class TestOAuth2ApplicationAdminFormInit(TestCase):
    """Unit tests for `OAuth2ApplicationAdminForm.__init__` method."""

    @patch("django.forms.ModelForm.__init__")
    def test_model_form_init_called(self, mock_super_init):
        """test_model_form_init_called"""
        with self.assertRaises(AttributeError):
            utils_forms.OAuth2ApplicationAdminForm()

        mock_super_init.assert_called()

    @patch.object(utils_forms, "forms")
    def test_client_type_not_required(self, mock_forms):
        """test_client_type_not_required"""
        oauth_app_object = utils_forms.OAuth2ApplicationAdminForm()
        self.assertFalse(oauth_app_object.fields["client_type"].required)

    @patch.object(utils_forms, "forms")
    def test_authorization_grant_type_not_required(self, mock_forms):
        """test_authorization_grant_type_not_required"""
        oauth_app_object = utils_forms.OAuth2ApplicationAdminForm()
        self.assertFalse(
            oauth_app_object.fields["authorization_grant_type"].required
        )

    @patch.object(utils_forms, "forms")
    def test_user_required(self, mock_forms):
        """test_user_required"""
        oauth_app_object = utils_forms.OAuth2ApplicationAdminForm()
        self.assertTrue(oauth_app_object.fields["user"].required)


class TestOAuth2ApplicationAdminFormSave(TestCase):
    """Unit tests for `OAuth2ApplicationAdminForm.save` method."""

    def setUp(self):
        """setUp"""
        self.mock_application_admin_form = (
            utils_forms.OAuth2ApplicationAdminForm()
        )
        self.mock_kwargs = {"commit": True}

    @patch("django.forms.ModelForm.save")
    def test_super_save_called(self, mock_model_form_save):
        """test_super_save_called"""
        self.mock_application_admin_form.save(**self.mock_kwargs)
        mock_model_form_save.assert_called_with(**self.mock_kwargs)

    @patch("django.forms.ModelForm.save")
    def test_client_type_is_set(self, mock_model_form_save):
        """test_client_type_is_set"""
        result = self.mock_application_admin_form.save(**self.mock_kwargs)
        self.assertEqual(
            result.client_type,
            utils_forms.OAuth2ApplicationAdminForm.Meta.forced_client_type,
        )

    @patch("django.forms.ModelForm.save")
    def test_authorization_grant_type_is_set(self, mock_model_form_save):
        """test_authorization_grant_type_is_set"""
        result = self.mock_application_admin_form.save(**self.mock_kwargs)
        self.assertEqual(
            result.authorization_grant_type,
            utils_forms.OAuth2ApplicationAdminForm.Meta.forced_authorization_grant_type,
        )

    @patch("django.forms.ModelForm.save")
    def test_save_not_called_if_commit_false(self, mock_model_form_save):
        """test_save_not_called_if_commit_false"""
        self.mock_kwargs["commit"] = False

        result = self.mock_application_admin_form.save(**self.mock_kwargs)
        result.save.assert_not_called()

    @patch("django.forms.ModelForm.save")
    def test_save_called_if_commit_true(self, mock_model_form_save):
        """test_save_called_if_commit_true"""
        self.mock_kwargs["commit"] = True

        result = self.mock_application_admin_form.save(**self.mock_kwargs)
        result.save.assert_called()
