""" Ajax admin
"""
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader

import core_federated_search_app.components.instance.api as instance_api
import core_federated_search_app.views.admin.forms as admin_forms
from core_federated_search_app.commons.exceptions import ExploreFederatedSearchAjaxError
from core_main_app.views.common.forms import RenameForm


def delete_repository(request):
    """ Delete repository.

    Returns:

    """
    try:
        instance = instance_api.get_by_id(request.GET['id'])
        instance_api.delete(instance)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')
    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_repository(request):
    """ Edit the repository.

    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            return _edit_repository_post(request)
        else:
            return _edit_repository_get(request)
    except Exception as e:
        return HttpResponseBadRequest(e.message)


def _edit_repository_get(request):
    """ Edit GET. Display the form

    Args:
        request:

    Returns:

    """
    context_params = dict()
    template = loader.get_template('core_federated_search_app/admin/repositories/list/modals/edit_form.html')
    data = {'id': request.GET['id'], 'field': request.GET['name']}
    rename_form = RenameForm(data)
    context_params['rename_form'] = rename_form
    context = {}
    context.update(request)
    context.update(context_params)
    return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')


def _edit_repository_post(request):
    """ Edit POST. Post the form

    Args:
        request:

    Returns:

    """
    try:
        form = RenameForm(request.POST)
        if form.is_valid():
            instance = instance_api.get_by_id(request.POST['id'])
            instance.name = request.POST['field']
            instance_api.upsert(instance)
        else:
            raise ExploreFederatedSearchAjaxError("All fields are required.")
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')
    return HttpResponse(json.dumps({}), content_type='application/javascript')


def refresh_repository(request):
    """ Refresh repository.

    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            return _refresh_repository_post(request)
        else:
            return _refresh_repository_get(request)
    except Exception as e:
        return HttpResponseBadRequest(e.message)


def _refresh_repository_post(request):
    """ POST request refresh repository.

    Args:
        request:

    Returns:

    """
    form = admin_forms.RefreshRepositoryForm(request.POST)
    if form.is_valid():
        try:
            repository_id = request.POST['id']
            instance = instance_api.get_by_id(repository_id)
        except:
            raise ExploreFederatedSearchAjaxError("Error: Unable to access the registered instance.")
        try:
            instance_api.refresh_instance_token(instance, request.POST["client_id"], request.POST["client_secret"],
                                                request.POST["timeout"])
            return HttpResponse(json.dumps({}), content_type='application/javascript')
        except Exception, e:
            raise ExploreFederatedSearchAjaxError(e.message)
    else:
        raise ExploreFederatedSearchAjaxError("All fields are required.")


def _refresh_repository_get(request):
    """ GET request refresh repository.

    Args:
        request:

    Returns:

    """
    context_params = dict()
    template = loader.get_template('core_federated_search_app/admin/repositories/list/refresh_form.html')
    refresh_form = admin_forms.RefreshRepositoryForm()
    context_params['refresh_form'] = refresh_form
    context = {}
    context.update(request)
    context.update(context_params)
    return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')
