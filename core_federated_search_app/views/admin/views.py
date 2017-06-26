""" Admin views Core explore Federated Search App
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from core_main_app.utils.rendering import admin_render
from core_federated_search_app.views.admin.forms import RepositoryForm
import core_main_app.commons.exceptions as common_exception
import core_federated_search_app.components.instance.api as api_instance


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
                instance_object = api_instance.add_instance(request.POST["name"], request.POST["endpoint"],
                                                            request.POST["client_id"], request.POST["client_secret"],
                                                            request.POST["username"], request.POST["password"],
                                                            request.POST["timeout"])
                if instance_object is not None:
                    return HttpResponseRedirect(reverse("admin:core_federated_search_app_repositories"))
            except common_exception.NotUniqueError:
                context['error'] = 'An instance with the same parameters already exists.'
            except Exception as api_exception:
                context['error'] = api_exception.message
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
