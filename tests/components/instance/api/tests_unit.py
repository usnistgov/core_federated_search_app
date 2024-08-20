""" Unit tests for `core_federated_search_app.components.api` package.
"""

from core_main_app.commons.exceptions import ApiError
import json
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from core_federated_search_app.components.instance import api as instance_api
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
            instance_api.get_blob_response_from_url("", "")

    @patch.object(instance_api, "send_get_request_with_token")
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
        return_value = instance_api.get_blob_response_from_url(
            "http://my.url.test", "http://my.url.test/098765432"
        )
        # assert
        self.assertEqual(return_value, "remote")


class TestCreateInstanceObjectFromRequestResponse(TestCase):
    def setUp(self) -> None:
        self.mock_name = "mock_instance_name"
        self.mock_endpoint = "http://mock_endpoint.example.com"
        self.mock_content = {
            "expires_in": 0,
            "refresh_token": "mock_refresh",
            "access_token": "mock_access",
        }

    def test_instance_name_is_correct(self):
        response = instance_api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(response.name, self.mock_name)

    def test_instance_endpoint_is_correct(self):
        response = instance_api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(response.endpoint, self.mock_endpoint)

    def test_instance_access_token_is_correct(self):
        response = instance_api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(
            response.access_token, self.mock_content["access_token"]
        )

    def test_instance_refresh_token_is_correct(self):
        response = instance_api._create_instance_object_from_request_response(
            self.mock_name, self.mock_endpoint, json.dumps(self.mock_content)
        )
        self.assertEqual(
            response.refresh_token, self.mock_content["refresh_token"]
        )

    def test_instance_expires_is_correct(self):
        response = instance_api._create_instance_object_from_request_response(
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

        response = instance_api._update_instance_object_from_request_response(
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

        instance_api._update_instance_token_from_response(
            mock_instance, mock_response
        )
        self.assertTrue(mock_upsert.called_with(mock_instance))


class TestAddInstance(TestCase):
    """Unit tests for `add_instance` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "name": MagicMock(),
            "endpoint": MagicMock(),
            "is_private_repo": MagicMock(),
            "client_id": MagicMock(),
            "client_secret": MagicMock(),
            "username": MagicMock(),
            "password": MagicMock(),
            "timeout": MagicMock(),
        }

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_urlparse_retrieve_endpoint(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_urlparse_retrieve_endpoint"""
        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        instance_api.add_instance(**self.mock_kwargs)

        mock_urlparse.assert_called_with(self.mock_kwargs["endpoint"])

    @patch.object(instance_api, "urlparse")
    def test_urlparse_error_raises_api_error(self, mock_urlparse):
        """test_urlparse_error_raises_api_error"""
        mock_urlparse.side_effect = Exception("mock_urlparse_exception")

        with self.assertRaises(ApiError):
            instance_api.add_instance(**self.mock_kwargs)

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_endpoint_name_is_striped(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_endpoint_name_is_string"""
        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        instance_api.add_instance(**self.mock_kwargs)

        self.mock_kwargs["name"].strip.is_called()

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_request_sent_to_endpoint(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_request_sent_to_endpoint"""
        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        instance_api.add_instance(**self.mock_kwargs)

        mock_post_request_token.assert_called_with(
            mock_endpoint_url,
            self.mock_kwargs["client_id"],
            self.mock_kwargs["client_secret"],
            self.mock_kwargs["timeout"],
            self.mock_kwargs["username"],
            self.mock_kwargs["password"],
        )

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_response_not_200_raises_api_error(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_response_not_200_raises_api_error"""
        mock_400_response = MockResponse()
        mock_400_response.status_code = 400
        mock_post_request_token.return_value = mock_400_response

        with self.assertRaises(ApiError):
            instance_api.add_instance(**self.mock_kwargs)

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_create_instance_is_called(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_create_instance_is_called"""
        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        instance_api.add_instance(**self.mock_kwargs)

        mock_create_instance_object_from_request_response.assert_called_with(
            mock_name, mock_endpoint_url, mock_200_response.content
        )

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "Instance")
    @patch.object(instance_api, "upsert")
    def test_public_repo_creates_instance(
        self,
        mock_upsert,
        mock_instance,
        mock_urlparse,
    ):
        """test_public_repo_creates_instance"""
        self.mock_kwargs["is_private_repo"] = False

        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        instance_api.add_instance(**self.mock_kwargs)

        mock_instance.assert_called_with(
            name=mock_name, endpoint=mock_endpoint_url
        )

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_upsert_is_called_for_private_repo(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_upsert_is_called_for_private_repo"""
        self.mock_kwargs["is_private_repo"] = True

        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        mock_instance_object = MagicMock()
        mock_create_instance_object_from_request_response.return_value = (
            mock_instance_object
        )

        instance_api.add_instance(**self.mock_kwargs)

        mock_upsert.assert_called_with(mock_instance_object)

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "Instance")
    @patch.object(instance_api, "upsert")
    def test_upsert_is_called_for_public_repo(
        self,
        mock_upsert,
        mock_instance,
        mock_urlparse,
    ):
        """test_upsert_is_called_for_public_repo"""
        self.mock_kwargs["is_private_repo"] = False

        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        mock_instance_object = MagicMock()
        mock_instance.return_value = mock_instance_object

        instance_api.add_instance(**self.mock_kwargs)

        mock_upsert.assert_called_with(mock_instance_object)

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "post_request_token")
    @patch.object(
        instance_api, "_create_instance_object_from_request_response"
    )
    @patch.object(instance_api, "upsert")
    def test_successful_exec_returns_instance_for_private_repo(
        self,
        mock_upsert,
        mock_create_instance_object_from_request_response,
        mock_post_request_token,
        mock_urlparse,
    ):
        """test_successful_exec_returns_instance_for_private_repo"""
        self.mock_kwargs["is_private_repo"] = True

        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        mock_200_response = MockResponse()
        mock_200_response.status_code = 200
        mock_post_request_token.return_value = mock_200_response

        mock_instance_object = MagicMock()
        mock_create_instance_object_from_request_response.return_value = (
            mock_instance_object
        )

        self.assertEqual(
            instance_api.add_instance(**self.mock_kwargs), mock_instance_object
        )

    @patch.object(instance_api, "urlparse")
    @patch.object(instance_api, "Instance")
    @patch.object(instance_api, "upsert")
    def test_successful_exec_returns_instance_for_public_repo(
        self,
        mock_upsert,
        mock_instance,
        mock_urlparse,
    ):
        """test_successful_exec_returns_instance_for_public_repo"""
        self.mock_kwargs["is_private_repo"] = False

        mock_endpoint_url = MagicMock()
        mock_urlparse().geturl().strip.return_value = mock_endpoint_url

        mock_name = MagicMock()
        self.mock_kwargs["name"].strip.return_value = mock_name

        mock_instance_object = MagicMock()
        mock_instance.return_value = mock_instance_object

        self.assertEqual(
            instance_api.add_instance(**self.mock_kwargs), mock_instance_object
        )
