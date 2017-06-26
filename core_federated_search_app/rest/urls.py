""" Url router for the REST API
"""
from django.conf.urls import url
from core_federated_search_app.rest.instance import views as instance_views


urlpatterns = [
    url(r'^instance/refresh', instance_views.refresh_token,
        name='core_federated_search_app_rest_instance_refresh'),

    url(r'^instance/delete$', instance_views.delete,
        name='core_federated_search_app_rest_instance_delete'),

    url(r'^instance/get$', instance_views.get_by_id,
        name='core_federated_search_app_rest_instance_get_by_id'),

    url(r'^instance', instance_views.instance,
        name='core_federated_search_app_rest_instance'),
]
