""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_federated_search_app.rest.instance import views as instance_views

urlpatterns = [
    re_path(
        r"^instance/$",
        instance_views.InstanceList.as_view(),
        name="core_federated_search_app_rest_instance",
    ),
    re_path(
        r"^instance/(?P<pk>\w+)/$",
        instance_views.InstanceDetail.as_view(),
        name="core_federated_search_app_rest_instance_detail",
    ),
    re_path(
        r"^instance/(?P<pk>\w+)/refresh/$",
        instance_views.InstanceRefreshToken.as_view(),
        name="core_federated_search_app_rest_instance_refresh",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
