""" Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site

from core_federated_search_app.components.instance.models import Instance
from core_federated_search_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)

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
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
