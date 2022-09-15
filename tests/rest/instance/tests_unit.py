"""Units tests for xsl Instance rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_federated_search_app.rest.instance.views as instance_views
from core_federated_search_app.components.instance.models import Instance


class TestGetAllInstanceList(SimpleTestCase):
    """Test Get All Instance List"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    @patch.object(Instance, "get_all")
    def test_get_all_returns_status_403_with_no_permission(self, mock_get_all):
        """test_get_all_returns_status_403_with_no_permission"""

        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Instance, "get_all")
    def test_get_all_returns_status_200_if_staff(self, mock_get_all):
        """test_get_all_returns_status_200_if_staff"""

        # Arrange
        user = create_mock_user("0", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPatchInstanceRefreshToken(SimpleTestCase):
    """TestPatchInstanceRefreshToken"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    @patch.object(Instance, "save_object")
    def test_patch_returns_status_403_if_user_is_not_admin(self, mock_save):
        """test_patch_returns_status_403_if_user_is_not_admin"""

        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceRefreshToken.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
