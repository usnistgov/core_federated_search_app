""" Admin views Core explore Federated Search App
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from core_main_app.utils.rendering import admin_render
from core_federated_search_app.views.admin.forms import RepositoryForm
from datetime import datetime, timedelta
from core_federated_search_app.components.instance.models import Instance
from core_explore_common_app.utils.protocols.oauth2 import post_request_token
import core_main_app.commons.exceptions as common_exception
import core_federated_search_app.components.instance.api as api_instance
import json


@staff_member_required
def manage_repositories(request):
    """ Manage repositories, Display as list.

    Args:
        request:

    Returns:

    """
    context = {
        'instance_list': api_instance.get_all()
    }

    modals = [
        "core_federated_search_app/admin/repositories/list/modals/edit.html",
        "core_federated_search_app/admin/repositories/list/modals/delete.html",
        "core_federated_search_app/admin/repositories/list/modals/refresh.html"
    ]

    assets = {
        "js": [
            {
                "path": 'core_federated_search_app/admin/js/repositories/list/modals/delete.js',
                "is_raw": False
            },
            {
                "path": 'core_federated_search_app/admin/js/repositories/list/modals/edit.js',
                "is_raw": False
            },
            {
                "path": 'core_federated_search_app/admin/js/repositories/list/modals/refresh.js',
                "is_raw": False
            }
        ]
    }

    return admin_render(request,
                        'core_federated_search_app/admin/repositories/list_repositories.html',
                        assets=assets,
                        context=context,
                        modals=modals)


@staff_member_required
def add_repository(request):
    """ Add new repository.

    Args:
        request:

    Returns:

    """
    context = {}
    new_form = False
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        context['repository_form'] = form
        if form.is_valid():
            try:
                url = request.POST["endpoint"]
                r = post_request_token(url, request.POST["client_id"], request.POST["client_secret"],
                                       request.POST["timeout"], request.POST["username"], request.POST["password"])

                if r.status_code == 200:
                    try:
                        instance = _create_instance(r.content, request.POST)
                        api_instance.upsert(instance)
                        return HttpResponseRedirect(reverse("admin:core_federated_search_app_repositories"))
                    except common_exception.NotUniqueError:
                        context['error'] = "An instance with the same parameters already exists."
                    except Exception as e:
                        context['error'] = e.message
                else:
                    context['error'] = "Unable to get access to the remote instance using these parameters."
            except Exception, e:
                context['error'] = "Unable to get access to the remote instance using these parameters."
    else:
        new_form = True

    if new_form:
        # render the form to upload a template
        context['repository_form'] = RepositoryForm()

    return admin_render(request,
                        'core_federated_search_app/admin/repositories/add_repository.html',
                        assets=None,
                        context=context,
                        modals=None)


def _create_instance(content, request):
    """ Create an Instance object from a request.

    Args:
        content:
        request:

    Returns:

    """
    now = datetime.now()
    delta = timedelta(seconds=int(json.loads(content)["expires_in"]))
    expires = now + delta
    return Instance(name=request["name"], endpoint=request['endpoint'],
                    access_token=json.loads(content)["access_token"],
                    refresh_token=json.loads(content)["refresh_token"], expires=expires)
