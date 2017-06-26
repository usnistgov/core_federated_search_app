""" REST Views for Instance object
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core_federated_search_app.rest.instance.serializers import InstanceSerializer
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
import core_federated_search_app.components.instance.api as instance_api


@api_view(['GET', 'POST'])
def instance(request):
    """ Instance rest api.

    GET /federated/search/rest/instance
    POST /federated/search/rest/instance

    Args:
        request:

    Returns:

    """
    if request.method == 'GET':
        return _get_all(request)
    elif request.method == 'POST':
        return _post(request)


def _get_all(request):
    """ Return http response with all instances.

    Args:
        request:

    Returns:

    """
    try:
        # Get object
        instance_object_list = instance_api.get_all()

        # Serialize object
        return_value = InstanceSerializer(instance_object_list, many=True)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_staff_member_required()
def _post(request):
    """ Save an instance.

        POST /federated/search/rest/instance
        {
            "name": "instance_name",
            "endpoint": "url",
            "client_id": "my_client_id",
            "client_secret": "my_client_secret",
            "timeout": "1",
            "username": "usr",
            "password": "pwd"
        }

        Args:
            request:

        Returns:

        """
    try:
        instance_object = instance_api.add_instance(request.data["name"], request.data["endpoint"],
                                                    request.data["client_id"], request.data["client_secret"],
                                                    request.data["username"], request.data["password"],
                                                    request.data["timeout"])
        if instance_object is not None:
            # Return the serialized instance
            return_value = InstanceSerializer(instance_object)
            return Response(return_value.data, status=status.HTTP_201_CREATED)
    except exceptions.NotUniqueError:
        content = {'message': 'An instance with the same parameters already exists.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@api_staff_member_required()
def delete(request):
    """ Delete instance by its id.

    /federated/search/rest/instance/delete?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        instance_id = request.query_params.get('id', None)

        # Check parameters
        if instance_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        instance_object = instance_api.get_by_id(instance_id)

        # Remove the instance
        instance_api.delete(instance_object)

        # Return response
        content = {'message': 'Instance deleted with success.'}
        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist as e:
        content = {'message': 'No instance found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_by_id(request):
    """ Get instance by its id.

        /federated/search/rest/instance/get?id=<id>

        Args:
            request:

        Returns:

        """
    try:
        # Get parameters
        instance_id = request.query_params.get('id', None)

        # Check parameters
        if instance_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        instance_object = instance_api.get_by_id(instance_id)

        # Serialize object
        return_value = InstanceSerializer(instance_object)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist as e:
        content = {'message': e.message}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions.ModelError, api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def refresh_token(request):
    """ Refresh token of an instance.

    POST /federated/search/rest/instance/refresh
    {
        "id": "instance_id",
        "client_id": "my_client_id",
        "client_secret": "my_client_secret",
        "timeout": "1"
    }

    Args:
        request:

    Returns:

    """
    try:
        repository_id = request.data['id']
        instance_object = instance_api.get_by_id(repository_id)
    except exceptions.DoesNotExist, e:
        content = {'message': e.message}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions.ModelError, api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        # refresh the token
        instance_object = instance_api.refresh_instance_token(instance_object, request.data["client_id"],
                                                              request.data["client_secret"], request.data["timeout"])
        # Serialize object
        return_value = InstanceSerializer(instance_object)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except Exception, api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
