"""Integration tests for instance rest api
"""
from bson import ObjectId
from rest_framework import status

import core_federated_search_app.rest.instance.views as instance_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.rest.instance.fixtures.fixtures import InstanceFixtures

fixture_data = InstanceFixtures()


class TestGetAllInstanceList(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestGetAllInstanceList, self).setUp()

    def test_get_all_returns_status_403_with_no_permission(self):
        # Arrange
        user = create_mock_user("1", is_anonymous=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_returns_status_403_if_staff(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetInstanceDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestGetInstanceDetail, self).setUp()
        self.data = None

    def test_get_returns_object_when_found(self):
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_get(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestDeleteInstanceDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestDeleteInstanceDetail, self).setUp()
        self.data = None

    def test_delete_raise_403_if_user_is_unauthorized(self):
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_return_204_if_document_is_deleted_whit_success(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_delete(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchInstanceDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestPatchInstanceDetail, self).setUp()
        self.data = None

    def test_patch_raise_403_if_user_is_authorized(self):
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_patch_returns_200_when_data_are_valid_with_authorized_user(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        self.data = {"name": "test_"}

        # Act
        response = RequestMock.do_request_patch(
            instance_views.InstanceDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
