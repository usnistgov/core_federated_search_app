from django.conf.urls import url, include
from django.contrib import admin
from core_federated_search_app import urls as core_federated_search_app_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + core_federated_search_app_urls.urlpatterns
