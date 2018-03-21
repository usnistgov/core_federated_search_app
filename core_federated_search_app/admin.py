""" Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url
from core_federated_search_app.views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^repositories/add', admin_views.add_repository,
        name='core_federated_search_app_repositories_add'),
    url(r'^repositories/delete', admin_ajax.delete_repository,
        name='core_federated_search_app_repositories_delete'),
    url(r'^repositories/(?P<pk>[\w-]+)/edit/$', admin_ajax.EditRepositoryView.as_view(),
        name='core_federated_search_app_repositories_edit'),
    url(r'^repositories/refresh', admin_ajax.refresh_repository,
        name='core_federated_search_app_repositories_refresh'),
    url(r'^repositories', admin_views.manage_repositories,
        name='core_federated_search_app_repositories'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
