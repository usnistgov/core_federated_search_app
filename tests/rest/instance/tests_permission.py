""" Authentication tests for Instance REST API
"""
import datetime

from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_federated_search_app.components.instance.models import Instance
from core_federated_search_app.rest.instance import views as instance_views
from core_federated_search_app.rest.instance.serializers import (
    InstanceSerializerModel,
    InstanceSerializerCreate,
)


class TestInstanceListGetPermission(SimpleTestCase):
    """Test Instance List Get Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_anonymous=True),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Instance, "get_all")
    @patch.object(InstanceSerializerModel, "data")
    def test_is_staff_returns_http_200(
        self, instance_serializer_data, instance_get_all
    ):
        """test_is_staff_returns_http_200"""

        instance_get_all.return_value = {}
        instance_serializer_data.return_value = True

        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_staff=True),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInstanceListPostPermission(SimpleTestCase):
    """Test Instance List Post Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_anonymous=True),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_post(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(InstanceSerializerCreate, "is_valid")
    @patch.object(InstanceSerializerCreate, "save")
    @patch.object(InstanceSerializerCreate, "data")
    def test_is_staff_returns_http_201(
        self,
        instance_serializer_data,
        instance_serializer_save,
        instance_serializer_is_valid,
    ):
        """test_is_staff_returns_http_201"""

        instance_serializer_is_valid.return_value = {}
        instance_serializer_save.return_value = None
        instance_serializer_data.return_value = True

        response = RequestMock.do_request_post(
            instance_views.InstanceList.as_view(),
            create_mock_user("1", is_staff=True),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestInstanceDetailGetPermission(SimpleTestCase):
    """Test Instance Detail Get Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Instance, "get_by_id")
    @patch.object(InstanceSerializerModel, "data")
    def test_is_staff_returns_http_200(
        self, instance_serializer_data, instance_get_all
    ):
        """test_is_staff_returns_http_200"""

        instance_get_all.return_value = {}
        instance_serializer_data.return_value = True

        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_staff=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInstanceDetailPatchPermission(SimpleTestCase):
    """Test Instance Detail Patch Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Instance, "get_by_id")
    @patch.object(InstanceSerializerModel, "is_valid")
    @patch.object(InstanceSerializerModel, "save")
    @patch.object(InstanceSerializerModel, "data")
    def test_is_staff_returns_http_200(
        self,
        instance_serializer_data,
        instance_serializer_save,
        instance_serializer_is_valid,
        instance_get_by_id,
    ):
        """test_is_staff_returns_http_200"""

        instance_get_by_id.return_value = {}
        instance_serializer_is_valid.return_value = {}
        instance_serializer_save.return_value = None
        instance_serializer_data.return_value = True

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInstanceDetailDeletePermission(SimpleTestCase):
    """Test Instance Detail Delete Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Instance, "delete")
    @patch.object(Instance, "get_by_id")
    def test_is_staff_returns_http_204(self, instance_get_by_id, instance_delete):
        """test_is_staff_returns_http_204"""

        instance_get_by_id.return_value = Instance(
            name="mock",
            endpoint="http://mock.com/",
            access_token="mock",
            refresh_token="mock",
            expires=datetime.datetime.now(),
        )

        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            create_mock_user("1", is_staff=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestInstanceRefreshTokenPatchPermission(SimpleTestCase):
    """Test Instance Refresh Token Patch Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            instance_views.InstanceRefreshToken.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403"""

        response = RequestMock.do_request_patch(
            instance_views.InstanceRefreshToken.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_federated_search_app.components.instance.api.refresh_instance_token")
    @patch.object(Instance, "get_by_id")
    @patch.object(InstanceSerializerModel, "is_valid")
    @patch.object(InstanceSerializerModel, "data")
    def test_is_staff_returns_http_200(
        self,
        instance_serializer_data,
        instance_serializer_is_valid,
        instance_get_by_id,
        instance_refresh_token,
    ):
        """test_is_staff_returns_http_200"""
        instance_get_by_id.return_value = {}
        instance_serializer_is_valid.return_value = {}
        instance_refresh_token.return_value = {}
        instance_serializer_data.return_value = True

        response = RequestMock.do_request_patch(
            instance_views.InstanceRefreshToken.as_view(),
            create_mock_user("1", is_staff=True),
            param={"pk": self.fake_id},
            data={
                "client_id": "my_client_id",
                "client_secret": "my_client_secret",
                "timeout": "1",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
