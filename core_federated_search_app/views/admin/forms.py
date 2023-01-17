""" Django forms of ADMIN core explore federated search
"""
from core_main_app.commons.validators import BlankSpacesValidator
from django import forms
from django.forms import ModelForm

from core_federated_search_app.components.instance.models import Instance

# list of possible protocols available in the form
PROTOCOLS = (("http", "HTTP"), ("https", "HTTPS"))


class RepositoryForm(forms.Form):
    """Form to register a new repository."""

    name = forms.CharField(
        label="Instance Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[BlankSpacesValidator()],
    )
    endpoint = forms.URLField(
        label="Endpoint",
        required=True,
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
    client_id = forms.CharField(
        label="Client ID",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    client_secret = forms.CharField(
        label="Client Secret",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    timeout = forms.IntegerField(
        label="Timeout (s)",
        min_value=1,
        max_value=60,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class RefreshRepositoryForm(forms.Form):
    """Form to refresh the token of a repository."""

    client_id = forms.CharField(
        label="Client ID",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    client_secret = forms.CharField(
        label="Client Secret",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    timeout = forms.IntegerField(
        label="Timeout (s)",
        min_value=1,
        max_value=60,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class EditRepositoryForm(ModelForm):
    """Form to edit repository"""

    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    class Meta:
        """Meta"""

        model = Instance
        fields = ["name"]
