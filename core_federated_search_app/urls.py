""" Url router for the federated search application
"""
from django.conf.urls import url, include


urlpatterns = [
    url(r'^rest/', include('core_federated_search_app.rest.urls')),
]
