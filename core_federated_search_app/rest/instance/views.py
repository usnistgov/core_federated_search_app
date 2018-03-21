""" REST Views for Instance object
"""
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_federated_search_app.components.instance.api as instance_api
from core_federated_search_app.rest.instance.serializers import InstanceSerializerCreate, InstanceSerializerModel
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required


class InstanceList(APIView):
    """ List all instances, or create a new instance.
    """

    def get(self, request):
        """ Return http response with all instances.

        GET /rest/instance

        Args:
            request:

        Returns:

        """
        try:
            # Get object
            instance_object_list = instance_api.get_all()

            # Serialize object
            return_value = InstanceSerializerModel(instance_object_list, many=True)

            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """ Save an instance.

        Example::

            POST /rest/instance
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
            # Build serializer
            instance_serializer = InstanceSerializerCreate(data=request.data)
            # Validate xsl
            instance_serializer.is_valid(True)
            # save or update the object
            instance_serializer.save()
            return Response(instance_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstanceDetail(APIView):
    """" Retrieve, edit or delete an instance.
    """

    def get_object(self, pk):
        """ Retrieve an instance

        Args:
            pk:

        Returns:

        """
        try:
            return instance_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Get instance by its id.

        GET /rest/instance/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Serialize object
            return_value = InstanceSerializerModel(instance_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {'message': 'Instance not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """ Update the instance

        Example::

            POST /rest/instance/pk
            {
                "name": "name"
            }

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Build serializer
            instance_serializer = InstanceSerializerModel(instance=instance_object,
                                                          data=request.data,
                                                          partial=True)
            # Validation
            instance_serializer.is_valid(True)
            # Save data
            instance_serializer.save()
            # Return response
            return Response(instance_serializer.data, status=status.HTTP_200_OK)
        except Http404:
            content = {'message': 'Instance not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def delete(self, request, pk):
        """ Delete instance by its id.

        DELETE /rest/instance/pk

        Args:
            pk:

        Returns:

        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Remove the instance
            instance_api.delete(instance_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {'message': 'Instance not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstanceRefreshToken(APIView):
    """" Refresh of token an instance.
    """

    def get_object(self, pk):
        """ Retrieve an instance

        Args:
            pk:

        Returns:

        """
        try:
            return instance_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """ Refresh token of an instance.

        Example::

            PATCH /rest/instance/pk/refresh
            {
                "client_id": "my_client_id",
                "client_secret": "my_client_secret",
                "timeout": "1"
            }

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            instance_object = self.get_object(pk)

            # refresh the token
            instance_object = instance_api.refresh_instance_token(instance_object, request.data["client_id"],
                                                                  request.data["client_secret"],
                                                                  request.data["timeout"])
            # Serialize object
            return_value = InstanceSerializerModel(instance_object)
            # Return response
            return Response(return_value.data, status=status.HTTP_200_OK)
        except Http404:
            content = {'message': 'Instance not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception, api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)