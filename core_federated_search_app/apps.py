""" Apps file for setting core package when app is ready.
"""

from django.apps import AppConfig


class CoreFederatedSearchAppConfig(AppConfig):
    """Core application settings."""

    name = "core_federated_search_app"
    verbose_name = "Core Federated Search App"
