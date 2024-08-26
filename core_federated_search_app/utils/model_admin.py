""" Model admins for definining admin GUI.
"""

from django.contrib import admin

from core_federated_search_app.utils.forms import OAuth2ApplicationAdminForm


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """Model admin considering all fields as read-only"""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OAuth2ApplicationAdmin(admin.ModelAdmin):
    """Model admin for django-oauth-toolkit `Application` model"""

    form = OAuth2ApplicationAdminForm
