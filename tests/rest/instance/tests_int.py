"""Integration tests for instance rest api
"""
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from rest_framework import status

import core_federated_search_app.rest.instance.views as instance_views
from tests.rest.instance.fixtures.fixtures import InstanceFixtures

fixture_data = InstanceFixtures()


class TestGetAllInstanceList(IntegrationBaseTestCase):
    """Test Get All Instance List"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_get_all_returns_status_403_with_no_permission(self):
        """test_get_all_returns_status_403_with_no_permission"""

        # Arrange
        user = create_mock_user("1", is_anonymous=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_returns_status_200_if_staff(self):
        """test_get_all_returns_status_200_if_staff"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetInstanceDetail(IntegrationBaseTestCase):
    """Test Get Instance Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_get_returns_object_when_found(self):
        """test_get_returns_object_when_found"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_raise_404_when_not_found(self):
        """test_get_raise_404_when_not_found"""

        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raise_500_sever_error_when_general_error_occurred(self):
        """test_get_raise_500_sever_error_when_general_error_occurred"""

        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestDeleteInstanceDetail(IntegrationBaseTestCase):
    """Test Delete Instance Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_delete_raise_403_if_user_is_unauthorized(self):
        """test_delete_raise_403_if_user_is_unauthorized"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": "1"}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_raise_404_when_not_found(self):
        """test_delete_raise_404_when_not_found"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_raise_500_sever_error_when_general_error_occurred(self):
        """test_post_raise_500_sever_error_when_general_error_occurred"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_post_return_204_if_document_is_deleted_whit_success(self):
        """test_post_return_204_if_document_is_deleted_whit_success"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchInstanceDetail(IntegrationBaseTestCase):
    """Test Patch Instance Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_patch_raise_403_if_user_is_authorized(self):
        """test_patch_raise_403_if_user_is_authorized"""

        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": "1"}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_raise_404_when_not_found(self):
        """test_patch_raise_404_when_not_found"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_raise_500_sever_error_when_general_error_occurred(self):
        """test_patch_raise_500_sever_error_when_general_error_occurred"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_patch_returns_200_when_data_are_valid_with_authorized_user(self):
        """test_patch_returns_200_when_data_are_valid_with_authorized_user"""

        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        self.data = {"name": "test_"}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
