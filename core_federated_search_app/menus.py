""" Federated search menu
"""
from django.urls import reverse
from menu import Menu, MenuItem


federated_children = (
    MenuItem(
        "Repositories",
        reverse("core-admin:core_federated_search_app_repositories"),
        icon="list",
    ),
    MenuItem(
        "Add Repository",
        reverse("core-admin:core_federated_search_app_repositories_add"),
        icon="plus-circle",
    ),
)

Menu.add_item(
    "admin", MenuItem("FEDERATED SEARCH", None, children=federated_children)
)
