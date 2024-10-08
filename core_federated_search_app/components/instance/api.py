""" Instance api
"""

import json
from urllib.parse import urlparse

from core_explore_common_app.utils.protocols.oauth2 import (
    post_request_token,
    post_refresh_token,
    send_get_request as send_get_request_with_token,
)
from core_federated_search_app.components.instance.models import Instance
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.datetime import datetime_now, datetime_timedelta


def get_all():
    """List all instance.

    Returns: instance collection

    """
    return Instance.get_all()


def get_by_id(instance_id):
    """Return instance object with the given id.

    Args:
        instance_id:

    Returns: instance object

    """
    return Instance.get_by_id(instance_id)


def get_by_name(instance_name):
    """Return instance object with the given name.

    Args:
        instance_name:

    Returns: instance object

    """
    return Instance.get_by_name(instance_name)


def get_by_endpoint_starting_with(instance_endpoint):
    """Return instance object with the given get_by_endpoint.

    Args:
        instance_endpoint:

    Returns: instance object

    """
    return Instance.get_by_endpoint_starting_with(instance_endpoint)


def delete(instance):
    """Delete an instance.

    Args:
        instance:

    Returns:

    """
    instance.delete()


def upsert(instance):
    """Update or save an instance.

    Args:
        instance:

    Returns:

    """
    instance.save_object()
    return instance


def add_instance(
    name,
    endpoint,
    is_private_repo,
    client_id,
    client_secret,
    username,
    password,
    timeout,
):
    """Request the remote and add the instance created.

    Args:
        name:
        endpoint:
        is_private_repo:
        client_id:
        client_secret:
        username:
        password:
        timeout:

    Returns:

    """
    try:
        # parse the endpoint
        endpoint_url = urlparse(endpoint).geturl().strip("/")
    except Exception:
        raise ApiError("Endpoint is not well formatted.")

    name = name.strip()  # Cleanup the instance name.

    # Request the remote
    if is_private_repo:
        response = post_request_token(
            endpoint_url, client_id, client_secret, timeout, username, password
        )

        if response.status_code != 200:
            raise ApiError(
                "Unable to get access to the remote instance using these parameters."
            )

        # create the instance from a request
        instance = _create_instance_object_from_request_response(
            name, endpoint_url, response.content
        )
    else:
        instance = Instance(name=name, endpoint=endpoint_url)

    # upsert the instance
    upsert(instance)
    return instance


def refresh_instance_token(instance, client_id, client_secret, timeout):
    """Refresh the instance token.

    Args:
        instance:
        client_id:
        client_secret:
        timeout:

    Returns:

    """
    # Request the remote
    response = post_refresh_token(
        instance.endpoint,
        client_id,
        client_secret,
        timeout,
        instance.refresh_token,
    )

    if response.status_code != 200:
        raise ApiError(
            "Unable to get access to the remote instance using these parameters."
        )

    # create the instance from a request
    instance = _update_instance_object_from_request_response(
        instance, response.content
    )

    # upsert the instance
    upsert(instance)
    return instance


def get_blob_response_from_url(url_base, url):
    """Get the blob response from an url

    Args:
        url_base: {uri.scheme}://{uri.netloc}
        url: full URL

    Returns:

    """
    # get instance from endpoint
    instance = get_by_endpoint_starting_with(url_base)
    if instance.endpoint in url:
        # here we are sure that our given url is one of our known instances
        return send_get_request_with_token(
            url=url, access_token=instance.access_token
        )


def _create_instance_object_from_request_response(name, endpoint, content):
    """Create an Instance object from a request.

    Args:
        name:
        endpoint:
        content:

    Returns:

    """
    # Calculate the expiration date
    now = datetime_now()
    delta = datetime_timedelta(seconds=int(json.loads(content)["expires_in"]))
    expires = now + delta
    # Create an instance with the response given by the remote server
    return Instance(
        name=name,
        endpoint=endpoint,
        access_token=json.loads(content)["access_token"],
        refresh_token=json.loads(content)["refresh_token"],
        expires=expires,
    )


def _update_instance_object_from_request_response(instance, content):
    """Update an instance object from a response content.

    Args:
        instance:
        content:

    Returns:

    """
    # Calculate the expiration date
    now = datetime_now()
    delta = datetime_timedelta(seconds=int(json.loads(content)["expires_in"]))
    expires = now + delta
    # Update an return the instance object
    instance.access_token = json.loads(content)["access_token"]
    instance.refresh_token = json.loads(content)["refresh_token"]
    instance.expires = expires
    return instance


def _get_url_for_request(instance):
    """Get an URL from an instance.

    Args:
        instance:

    Returns:

    """
    return (
        instance.protocol
        + "://"
        + instance.address
        + ":"
        + str(instance.port)
        + "/o/token/"
    )


def _update_instance_token_from_response(instance, response):
    """Update an instance token from an http response.

    Args:
        instance:
        response:

    Returns:

    """
    data = response.json()
    now = datetime_now()
    delta = datetime_timedelta(seconds=int(data["expires_in"]))
    instance.refresh_token = data["refresh_token"]
    instance.expires = now + delta
    instance.access_token = data["access_token"]
    upsert(instance)
