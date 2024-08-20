""" Admin views Core explore Federated Search App
"""

import core_main_app.commons.exceptions as common_exception
from core_main_app.utils.rendering import admin_render
from core_main_app.views.common.ajax import EditTemplateVersionManagerView
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from requests.exceptions import SSLError

import core_federated_search_app.components.instance.api as api_instance
from core_federated_search_app.views.admin.forms import RepositoryForm


@staff_member_required
def manage_repositories(request):
    """Manage repositories, Display as list.

    Args:
        request:

    Returns:

    """
    context = {"instance_list": api_instance.get_all()}

    modals = [
        "core_federated_search_app/admin/repositories/list/modals/delete.html",
        "core_federated_search_app/admin/repositories/list/modals/refresh.html",
        EditTemplateVersionManagerView.get_modal_html_path(),
    ]

    assets = {
        "js": [
            {
                "path": "core_federated_search_app/admin/js/repositories/list/modals/delete.js",
                "is_raw": False,
            },
            {
                "path": "core_federated_search_app/admin/js/repositories/list/modals/refresh.js",
                "is_raw": False,
            },
            EditTemplateVersionManagerView.get_modal_js_path(),
        ],
        "css": ["core_federated_search_app/admin/css/repositories.css"],
    }

    return admin_render(
        request,
        "core_federated_search_app/admin/repositories/list_repositories.html",
        assets=assets,
        context=context,
        modals=modals,
    )


@staff_member_required
def add_repository(request):
    """Add new repository.

    Args:
        request:

    Returns:

    """
    context = {}
    if request.method == "POST":
        form = RepositoryForm(request.POST)

        context["repository_form"] = form
        if form.is_valid():
            try:
                instance_object = api_instance.add_instance(
                    form.data["name"],
                    form.data["endpoint"],
                    bool(form.data.get("is_private_repo", None)),
                    form.data["client_id"],
                    form.data["client_secret"],
                    form.data["username"],
                    form.data["password"],
                    form.data["timeout"],
                )
                if instance_object is not None:
                    return HttpResponseRedirect(
                        reverse(
                            "core-admin:core_federated_search_app_repositories"
                        )
                    )
            except common_exception.NotUniqueError:
                context["error"] = (
                    "An instance with the same parameters already exists."
                )
            except SSLError:
                context["error"] = "Unable to reach the remote HTTPS instance."
            except Exception as api_exception:
                context["error"] = str(api_exception)
        else:
            context["error"] = "The form entered is not valid."
    else:
        # render the form to upload a template
        context["repository_form"] = RepositoryForm()

    assets = {
        "js": [
            {
                "path": "core_federated_search_app/admin/js/repositories/add/form.js",
                "is_raw": False,
            },
        ],
        "css": ["core_federated_search_app/admin/css/add/form.css"],
    }

    return admin_render(
        request,
        "core_federated_search_app/admin/repositories/add_repository.html",
        assets=assets,
        context=context,
        modals=None,
    )
