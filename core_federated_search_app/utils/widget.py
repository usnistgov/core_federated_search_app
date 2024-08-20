""" Widget utilities for forms.
"""

from django.forms.widgets import CheckboxInput


class ToggleButton(CheckboxInput):
    """A checkbox input designed as a toggle button."""

    input_type = "checkbox"
    template_name = "forms/widgets/toggle_button.html"

    def __init__(self, attrs=None):
        """Setup the widget.

        Args:
            attrs:
        """
        super().__init__(attrs)
        self.attrs.update({"class": "form-check-input", "role": "switch"})
