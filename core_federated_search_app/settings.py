""" Settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

CUSTOM_NAME = getattr(settings, 'CUSTOM_NAME', 'Local')
""" :py:class:`str`: Name of the local instance
"""
