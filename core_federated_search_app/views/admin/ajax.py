""" Ajax admin
"""
import json

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader

import core_federated_search_app.components.instance.api as instance_api
import core_federated_search_app.views.admin.forms as admin_forms
from core_federated_search_app.commons.exceptions import ExploreFederatedSearchAjaxError
from core_federated_search_app.components.instance.models import Instance
from core_federated_search_app.views.admin.forms import EditRepositoryForm
from core_main_app.views.common.ajax import EditObjectModalView


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


class EditRepositoryView(EditObjectModalView):
    form_class = EditRepositoryForm
    model = Instance
    success_url = reverse_lazy("admin:core_federated_search_app_repositories")

    def _save(self, form):
        # Save treatment.
        # It should return an HttpResponse.
        try:
            instance_api.upsert(self.object)
            messages.add_message(self.request, messages.SUCCESS, 'Repository edited with success.')
        except Exception, e:
            form.add_error(None, e.message)
            return super(EditRepositoryView, self).form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


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
