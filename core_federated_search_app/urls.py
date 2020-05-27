""" Url router for the federated search application
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r"^rest/", include("core_federated_search_app.rest.urls")),
]
