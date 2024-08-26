""" Model forms for definining admin GUI.
"""

from django.contrib import admin
from django import forms
from oauth2_provider.models import get_application_model, AbstractApplication

from core_federated_search_app.utils.widgets import (
    UnprivilegedUserWidget,
    ReadOnlyTextWidget,
)


class OAuth2ApplicationAdminForm(forms.ModelForm):
    """Form for django-oauth-toolkit `Application` model."""

    def __init__(self, *args, **kwargs):
        super(OAuth2ApplicationAdminForm, self).__init__(*args, **kwargs)
        self.fields["client_type"].required = False
        self.fields["authorization_grant_type"].required = False
        self.fields["user"].required = True

    class Meta:
        forced_client_type = AbstractApplication.CLIENT_CONFIDENTIAL
        forced_authorization_grant_type = AbstractApplication.GRANT_PASSWORD

        model = get_application_model()
        fields = (
            "client_id",
            "client_secret",
            "user",
            "client_type",
            "authorization_grant_type",
            "algorithm",
            "redirect_uris",
            "post_logout_redirect_uris",
            "allowed_origins",
        )
        widgets = {
            "user": UnprivilegedUserWidget(
                rel=get_application_model()
                ._meta.get_field("user")
                .remote_field,
                admin_site=admin.site,
            ),
            "client_type": ReadOnlyTextWidget(
                default_value=dict(AbstractApplication.CLIENT_TYPES)[
                    forced_client_type
                ]
            ),
            "authorization_grant_type": ReadOnlyTextWidget(
                default_value=dict(AbstractApplication.GRANT_TYPES)[
                    forced_authorization_grant_type
                ]
            ),
        }

    def save(self, commit=True):
        instance = super(OAuth2ApplicationAdminForm, self).save(commit=commit)
        instance.client_type = self.Meta.forced_client_type
        instance.authorization_grant_type = (
            self.Meta.forced_authorization_grant_type
        )

        if commit:
            instance.save()

        return instance
