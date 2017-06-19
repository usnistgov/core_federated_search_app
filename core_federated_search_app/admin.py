""" Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

admin_urls = [
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
