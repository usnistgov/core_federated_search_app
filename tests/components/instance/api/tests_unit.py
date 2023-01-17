""" Boolean utils test class
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock

from core_federated_search_app.components.instance import api
from core_federated_search_app.components.instance.models import Instance
from core_main_app.commons import exceptions
from core_main_app.utils.datetime import datetime_now, datetime_timedelta
from tests.mocks import MockResponse


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


class Test_create_instance_object_from_request_response(TestCase):
    def setUp(self) -> None:
        self.mock_name = "mock_instance_name"
        self.mock_endpoint = "http://mock_endpoint.example.com"
        self.mock_content = {
            "expires_in": 0,
            "refresh_token": "mock_refresh",
            "access_token": "mock_access",
        }

    def test_instance_name_is_correct(self):
        response = api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(response.name, self.mock_name)

    def test_instance_endpoint_is_correct(self):
        response = api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(response.endpoint, self.mock_endpoint)

    def test_instance_access_token_is_correct(self):
        response = api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(
            response.access_token, self.mock_content["access_token"]
        )

    def test_instance_refresh_token_is_correct(self):
        response = api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(
            response.refresh_token, self.mock_content["refresh_token"]
        )

    def test_instance_expires_is_correct(self):
        response = api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertLessEqual(
            response.expires,
            datetime_now()
            + datetime_timedelta(seconds=self.mock_content["expires_in"]),
        )


class TestUpdateInstanceObjectFromRequestResponse(TestCase):
    def test_instance_is_returned(self):
        mock_instance = Mock()
        mock_content = json.dumps(
            {
                "expires_in": 0,
                "refresh_token": "mock_refresh",
                "access_token": "mock_access",
            }
        )

        response = api._update_instance_object_from_request_response(
            mock_instance, mock_content
        )
        self.assertEqual(response, mock_instance)


class TestUpdateInstanceTokenFromResponse(TestCase):
    @patch("core_federated_search_app.components.instance.api.upsert")
    def test_instance_is_updated(self, mock_upsert):
        mock_data = json.dumps(
            {
                "expires_in": 0,
                "refresh_token": "mock_refresh",
                "access_token": "mock_access",
            }
        )

        mock_instance = Mock()
        mock_response = MockResponse()
        mock_response.data = mock_data

        api._update_instance_token_from_response(mock_instance, mock_response)
        self.assertTrue(mock_upsert.called_with(mock_instance))
