"""Units tests for xsl Instance rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

import core_federated_search_app.rest.instance.views as instance_views
from core_federated_search_app.components.instance.models import Instance
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGetAllInstanceList(SimpleTestCase):
    def setUp(self):
        super(TestGetAllInstanceList, self).setUp()
        self.data = None

    @patch.object(Instance, "get_all")
    def test_get_all_returns_status_403_with_no_permission(self, mock_get_all):
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
        # Arrange
        user = create_mock_user("0", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPatchInstanceRefreshToken(SimpleTestCase):
    def setUp(self):
        super(TestPatchInstanceRefreshToken, self).setUp()
        self.data = None

    @patch.object(Instance, "save_object")
    def test_patch_returns_status_403_if_user_is_not_admin(self, mock_save):
        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceRefreshToken.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
