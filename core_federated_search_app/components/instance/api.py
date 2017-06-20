""" Instance api
"""
import requests
from datetime import datetime
from core_federated_search_app.components.instance.models import Instance
from core_main_app.commons.exceptions import ApiError


def get_all():
    """ List all instance.

    Returns: instance collection

    """
    return Instance.get_all()


def get_by_id(instance_id):
    """ Return instance object with the given id.

    Args:
        instance_id:

    Returns: instance object

    """
    return Instance.get_by_id(instance_id)


def get_by_name(instance_name):
    """ Return instance object with the given name.

    Args:
        instance_name:

    Returns: instance object

    """
    return Instance.get_by_name(instance_name)


def delete(instance):
    """ Delete an instance.

    Args:
        instance:

    Returns:

    """
    instance.delete()


def upsert(instance):
    """ Update or save an instance.

    Args:
        instance:

    Returns:

    """
    return instance.save_object()


def request_token(instance, client_id, client_secret, timeout=1000):
    """ Create the instance by requesting a token.

    Args:
        instance:
        client_id:
        client_secret:
        timeout:

    Returns:

    """
    url = _get_url_for_request(instance)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'password',
        'username': instance.username,
        'password': instance.password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(url=url, data=data, headers=headers, timeout=timeout)
    if response.status_code == 200:
        _update_instance_token_from_response(instance, response)
    else:
        raise ApiError("Unable to get access to the remote instance using these parameters.")


def refresh_token(instance, timeout=1000):
    """ Refresh the instance token.

    Args:
        instance:
        timeout:

    Returns:

    """
    url = _get_url_for_request(instance)
    data = "&grant_type=refresh_token&refresh_token=" + instance.refresh_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url=url, data=data,
                             headers=headers,
                             auth=(instance.client_id, instance.client_secret),
                             timeout=timeout)
    if response.status_code == 200:
        _update_instance_token_from_response(instance, response)
    else:
        raise ApiError("Unable to get access to the remote instance using these parameters.")


def _get_url_for_request(instance):
    """ Get an URL from an instance.

    Args:
        instance:

    Returns:

    """
    return instance.protocol + "://" + instance.address + ":" + str(instance.port) + "/o/token/"


def _update_instance_token_from_response(instance, response):
    """ Update an instance token from an http response.

    Args:
        instance:
        response:

    Returns:

    """
    data = response.json()
    now = datetime.now()
    delta = datetime.timedelta(seconds=int(data['expires_in']))
    instance.refresh_token = data['refresh_token']
    instance.expires = now + delta
    instance.access_token = data['access_token']
    upsert(instance)
