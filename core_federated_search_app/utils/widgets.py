""" Widget utilities for forms.
"""

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.forms.widgets import CheckboxInput, Widget


class ToggleButton(CheckboxInput):
    """A checkbox input designed as a toggle button."""

    input_type = "checkbox"
    template_name = "forms/widgets/toggle_button.html"

    def __init__(self, attrs=None):
        """Setup the widget."""
        super().__init__(attrs)
        self.attrs.update({"class": "form-check-input", "role": "switch"})


class UnprivilegedUserWidget(ForeignKeyRawIdWidget):
    """A widget to only be able to select unprivileged users."""

    def __init__(self, *args, **kwargs):
        """Widget initialization. Limit the selection to unprivileged users."""
        super().__init__(*args, **kwargs)
        self.rel_label = "User"
        self.rel.limit_choices_to = {
            "is_active": True,
            "is_superuser": False,
            "is_staff": False,
        }


class ReadOnlyTextWidget(Widget):
    """A widget to only display a value with no possibility of modification"""

    def __init__(self, default_value, *args, **kwargs):
        """Widget initialization. Allows for setting up the value that will be displayed
        in the form.
        """
        super().__init__(*args, **kwargs)
        self.default_value = default_value

    def render(self, name, value, attrs=None, renderer=None):
        """Renders the widget."""
        return f"<div style='align-content: center'>{self.default_value}</div>"
