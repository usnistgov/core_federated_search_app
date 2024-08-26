""" Url router for the administration site
"""

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path
from oauth2_provider.models import (
    get_application_model,
    get_grant_model,
    get_id_token_model,
    get_access_token_model,
    get_refresh_token_model,
)

from core_federated_search_app.components.instance.models import Instance
from core_federated_search_app.utils.model_admin import (
    OAuth2ApplicationAdmin,
    ReadOnlyModelAdmin,
)
from core_federated_search_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)
from core_main_app.admin import core_admin_site

admin_urls = [
    re_path(
        r"^repositories/add",
        admin_views.add_repository,
        name="core_federated_search_app_repositories_add",
    ),
    re_path(
        r"^repositories/delete",
        admin_ajax.delete_repository,
        name="core_federated_search_app_repositories_delete",
    ),
    re_path(
        r"^repositories/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditRepositoryView.as_view()),
        name="core_federated_search_app_repositories_edit",
    ),
    re_path(
        r"^repositories/refresh",
        admin_ajax.refresh_repository,
        name="core_federated_search_app_repositories_refresh",
    ),
    re_path(
        r"^repositories",
        admin_views.manage_repositories,
        name="core_federated_search_app_repositories",
    ),
]

admin.site.register(Instance)

# Remove unused django-oauth-toolkit models.
admin.site.unregister(get_id_token_model())
admin.site.unregister(get_grant_model())

# Register django-oauth-toolkit `Application` with appropriate model admin.
admin.site.unregister(get_application_model())
admin.site.register(get_application_model(), OAuth2ApplicationAdmin)

# Register django-oauth-toolkit `AccessToken` with appropriate model admin.
admin.site.unregister(get_access_token_model())
admin.site.register(get_access_token_model(), ReadOnlyModelAdmin)

# Register django-oauth-toolkit `RefreshToken` with appropriate model admin.
admin.site.unregister(get_refresh_token_model())
admin.site.register(get_refresh_token_model(), ReadOnlyModelAdmin)

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
