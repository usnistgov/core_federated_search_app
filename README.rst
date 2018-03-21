=========================
Core Federated Search App
=========================

Federated search backend for the curator core project.

Quick start
===========

1. Add "core_federated_search_app" to your INSTALLED_APPS setting
-----------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      'oauth2_provider',
      'core_federated_search_app',
    ]

2. Include the core_federated_search_app URLconf in your project urls.py
------------------------------------------------------------------------

.. code:: python

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^federated/search/', include("core_federated_search_app.urls")),
