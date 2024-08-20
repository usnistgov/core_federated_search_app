""" Unit tests for `core_federated_search_app.components.instance.models` package.
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.db import IntegrityError

from core_federated_search_app.components.instance import (
    models as instance_models,
)
from core_main_app.commons.exceptions import ModelError, NotUniqueError


class TestSaveObject(TestCase):
    """Unit tests for `save_object` method"""

    def setUp(self):
        """setUp"""
        self.mock_instance_object = instance_models.Instance()

    @patch.object(instance_models.Instance, "check_instance_name")
    def test_check_instance_name_called(self, mock_check_instance_name):
        """test_check_instance_name_called"""
        self.mock_instance_object.save_object()
        mock_check_instance_name.assert_called()

    @patch.object(instance_models.Instance, "check_instance_name")
    @patch.object(instance_models, "logging")
    def test_check_instance_exception_raises_model_error(
        self, mock_logging, mock_check_instance_name
    ):
        """test_check_instance_exception_raises_model_error"""
        mock_check_instance_name.side_effect = Exception(
            "mock_check_instance_name_exception"
        )

        with self.assertRaises(ModelError):
            self.mock_instance_object.save_object()

    @patch.object(instance_models.Instance, "check_instance_name")
    @patch.object(instance_models.Instance, "save")
    def test_save_called(self, mock_save, mock_check_instance_name):
        """test_save_called"""
        self.mock_instance_object.save_object()
        mock_save.assert_called()

    @patch.object(instance_models.Instance, "check_instance_name")
    @patch.object(instance_models.Instance, "save")
    @patch.object(instance_models, "logging")
    def test_save_exception_raises_model_error(
        self, mock_logging, mock_save, mock_check_instance_name
    ):
        """test_save_exception_raises_model_error"""
        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(ModelError):
            self.mock_instance_object.save_object()

    @patch.object(instance_models.Instance, "check_instance_name")
    @patch.object(instance_models.Instance, "save")
    @patch.object(instance_models, "logging")
    def test_save_integrity_error_raises_not_unique_error(
        self, mock_logging, mock_save, mock_check_instance_name
    ):
        """test_save_integrity_error_raises_not_unique_error"""
        mock_check_instance_name.side_effect = IntegrityError(
            "mock_check_instance_name_exception"
        )

        with self.assertRaises(NotUniqueError):
            self.mock_instance_object.save_object()

    @patch.object(instance_models.Instance, "check_instance_name")
    @patch.object(instance_models.Instance, "save")
    def test_returns_save_output(self, mock_save, mock_check_instance_name):
        """test_returns_save_output"""
        expected_output = MagicMock()
        mock_save.return_value = expected_output

        self.assertEqual(
            self.mock_instance_object.save_object(), expected_output
        )


class TestClean(TestCase):
    """Unit tests for `clean` method."""

    def test_return_striped_input(self):
        """test_return_striped_input"""
        orig_name = "   mock_name    "
        mock_instance = instance_models.Instance()
        mock_instance.name = orig_name

        mock_instance.clean()

        self.assertEqual(mock_instance.name, str(orig_name).strip())
