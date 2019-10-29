SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",

    # Local app
    "tests",
]

CUSTOM_NAME = 'Local'
""" :py:class:`str`: Name of the local instance
"""
