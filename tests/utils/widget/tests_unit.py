""" Unit tests for `core_federated_search_app.utils.widget` package.
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_federated_search_app.utils import widgets


class TestToggleButton(TestCase):
    """Unit tests for `ToggleButton` widget."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"attrs": None}

    def test_input_type_checkbox(self):
        """test_input_type_checkbox"""
        mock_toggle_button = widgets.ToggleButton()
        self.assertEqual(mock_toggle_button.input_type, "checkbox")

    def test_template_name_set(self):
        """test_template_name_set"""
        mock_toggle_button = widgets.ToggleButton()
        self.assertEqual(
            mock_toggle_button.template_name,
            "forms/widgets/toggle_button.html",
        )

    @patch("django.forms.widgets.CheckboxInput.__init__")
    def test_checkbox_input_init_called(self, mock_checkbox_input_init):
        """test_checkbox_input_init_called"""
        with self.assertRaises(AttributeError):
            widgets.ToggleButton()

        mock_checkbox_input_init.assert_called()

    def test_attributes_updated(self):
        """test_attributes_updated"""
        mock_toggle_button = widgets.ToggleButton()
        self.assertIn("class", mock_toggle_button.attrs)
        self.assertIn("role", mock_toggle_button.attrs)
        self.assertEqual(mock_toggle_button.attrs["class"], "form-check-input")
        self.assertEqual(mock_toggle_button.attrs["role"], "switch")


class TestUnprivilegedUserWidget(TestCase):
    """Unit tests for `UnprivilegedUserWidget` widget."""

    def setUp(self):
        self.mock_kwargs = {"rel": MagicMock(), "admin_site": MagicMock()}

    @patch("django.contrib.admin.widgets.ForeignKeyRawIdWidget.__init__")
    def test_foreign_key_raw_id_widget_init_called(
        self, mock_foreign_key_raw_id_widget_init
    ):
        """test_foreign_key_raw_id_widget_init_called"""
        with self.assertRaises(AttributeError):
            widgets.UnprivilegedUserWidget(**self.mock_kwargs)

        mock_foreign_key_raw_id_widget_init.assert_called()

    def test_rel_label_set(self):
        """test_rel_label_set"""
        mock_widget = widgets.UnprivilegedUserWidget(**self.mock_kwargs)
        self.assertEqual(mock_widget.rel_label, "User")

    def test_rel_limit_choice_to_set(self):
        """test_rel_limit_choice_to_set"""
        mock_widget = widgets.UnprivilegedUserWidget(**self.mock_kwargs)
        self.assertEqual(
            mock_widget.rel.limit_choices_to,
            {
                "is_active": True,
                "is_superuser": False,
                "is_staff": False,
            },
        )


class TestReadOnlyTextWidget(TestCase):
    """Unit tests for `ReadOnlyTextWidget` widget."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"default_value": MagicMock()}

    @patch("django.forms.widgets.Widget.__init__")
    def test_widget_init_called(self, mock_widget_init):
        """test_widget_init_called"""
        widgets.ReadOnlyTextWidget(**self.mock_kwargs)

        mock_widget_init.assert_called()

    def test_default_value_set(self):
        """test_default_value_set"""
        mock_widget = widgets.ReadOnlyTextWidget(**self.mock_kwargs)

        self.assertEqual(
            mock_widget.default_value, self.mock_kwargs["default_value"]
        )

    def test_render_returns_correct_string(self):
        """test_render_returns_correct_string"""
        mock_widget = widgets.ReadOnlyTextWidget(**self.mock_kwargs)

        self.assertEqual(
            mock_widget.render("mock_name", "mock_value"),
            f"<div style='align-content: center'>{self.mock_kwargs['default_value']}</div>",
        )
