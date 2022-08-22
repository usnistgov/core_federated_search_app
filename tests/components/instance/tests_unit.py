""" Boolean utils test class
"""
from unittest import TestCase

from mock import patch

from core_main_app.commons import exceptions
from core_federated_search_app.components.instance import api
from core_federated_search_app.components.instance.models import Instance


class TestGetBlobResponseFromUrl(TestCase):
    """Test Get Blob Response From Url"""

    def test_get_blob_response_from_url_raise_exception_if_url_is_not_known_instance(
        self,
    ):
        """test_get_blob_response_from_url_raise_exception_if_url_is_not_known_instance"""

        # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            # Arrange / Act
            api.get_blob_response_from_url("", "")

    @patch(
        "core_main_app.utils.requests_utils.requests_utils.send_get_request_with_access_token"
    )
    @patch(
        "core_federated_search_app.components.instance.api.get_by_endpoint_starting_with"
    )
    def test_get_blob_response_from_url_return_blob_if_is_known_instance(
        self,
        mock_get_by_endpoint_starting_with,
        mock_send_get_request_with_access_token,
    ):
        """test_get_blob_response_from_url_return_blob_if_is_known_instance"""

        # Arrange
        mock_get_by_endpoint_starting_with.return_value = Instance(
            name="name",
            endpoint="http://my.url.test",
            access_token="access_token",
            refresh_token="refresh_token",
            expires="date",
        )

        mock_send_get_request_with_access_token.return_value = "remote"

        # Act
        return_value = api.get_blob_response_from_url(
            "http://my.url.test", "http://my.url.test/098765432"
        )
        # assert
        self.assertEqual(return_value, "remote")
