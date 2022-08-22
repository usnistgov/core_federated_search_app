""" REST Views for Instance object
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
import core_federated_search_app.components.instance.api as instance_api
from core_federated_search_app.rest.instance.serializers import (
    InstanceSerializerCreate,
    InstanceSerializerModel,
)


class InstanceList(APIView):
    """List all Instances, or create a new Instance"""

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Return http response with all Instances

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of Instances
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            instance_object_list = instance_api.get_all()

            # Serialize object
            return_value = InstanceSerializerModel(instance_object_list, many=True)

            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Save an Instance

        Parameters:

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

            request: HTTP request

        Returns:

            - code: 201
              content: Created Instance
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
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
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstanceDetail(APIView):
    """ " Retrieve, edit or delete an Instance"""

    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        """Retrieve an Instance

        Args:

            pk: ObjectId

        Returns:

            Instance
        """
        try:
            return instance_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Get Instance

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Instance
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Serialize object
            return_value = InstanceSerializerModel(instance_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {"message": "Instance not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """Update the Instance

        Parameters:

            {
                "name": "name"
            }

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Updated Instance
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Build serializer
            instance_serializer = InstanceSerializerModel(
                instance=instance_object, data=request.data, partial=True
            )
            # Validation
            instance_serializer.is_valid(True)
            # Save data
            instance_serializer.save()
            # Return response
            return Response(instance_serializer.data, status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Instance not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete Instance

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            instance_object = self.get_object(pk)
            # Remove the instance
            instance_api.delete(instance_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {"message": "Instance not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstanceRefreshToken(APIView):
    """ " Refresh of token an Instance"""

    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        """Retrieve an Instance

        Args:

            pk: ObjectId

        Returns:

            Instance
        """
        try:
            return instance_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        """Refresh token of an Instance

        Parameters:

            {
                "client_id": "my_client_id",
                "client_secret": "my_client_secret",
                "timeout": "1"
            }

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Updated Instance
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            instance_object = self.get_object(pk)

            # refresh the token
            instance_object = instance_api.refresh_instance_token(
                instance_object,
                request.data["client_id"],
                request.data["client_secret"],
                request.data["timeout"],
            )
            # Serialize object
            return_value = InstanceSerializerModel(instance_object)
            # Return response
            return Response(return_value.data, status=status.HTTP_200_OK)
        except Http404:
            content = {"message": "Instance not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
