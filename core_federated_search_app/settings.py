""" Settings core_federated_search_app

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

CUSTOM_NAME = getattr(settings, "CUSTOM_NAME", "Local")
""" :py:class:`str`: Name of the local instance
"""
