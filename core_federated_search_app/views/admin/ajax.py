""" Ajax admin
"""
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader
from datetime import datetime, timedelta
from core_explore_common_app.utils.protocols.oauth2 import post_refresh_token
from core_federated_search_app.commons.exceptions import ExploreFederatedSearchAjaxError
import core_federated_search_app.views.admin.forms as admin_forms
import core_federated_search_app.components.instance.api as instance_api
import json


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
        instance = instance_api.get_by_id(request.POST['id'])
        instance.name = request.POST['title']
        instance_api.upsert(instance)
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
            r = post_refresh_token(instance.endpoint, request.POST["client_id"], request.POST["client_secret"],
                                   request.POST["timeout"], instance.refresh_token)

            if r.status_code == 200:
                instance = _update_instance(instance, r.content)
                instance_api.upsert(instance)
                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                raise ExploreFederatedSearchAjaxError("Unable to get access to the "
                                                      "remote instance using these parameters.")
        except Exception, e:
            raise ExploreFederatedSearchAjaxError("Unable to get access to the remote instance using these parameters.")
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
    context = RequestContext(request, context_params)
    return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')


def _update_instance(instance, content):
    """ Update an instance object from a response content.

    Args:
        instance:
        content:

    Returns:

    """
    now = datetime.now()
    delta = timedelta(seconds=int(json.loads(content)["expires_in"]))
    expires = now + delta
    instance.access_token = json.loads(content)["access_token"]
    instance.refresh_token = json.loads(content)["refresh_token"]
    instance.expires = expires
    return instance
