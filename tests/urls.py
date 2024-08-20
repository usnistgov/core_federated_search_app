""" Url router for the administration site
"""

from django.urls import re_path

from core_federated_search_app.views.admin import (
    views as admin_views,
)

urlpatterns = [
    re_path(
        r"^repositories/add",
        admin_views.add_repository,
        name="core_federated_search_app_repositories_add",
    )
]
