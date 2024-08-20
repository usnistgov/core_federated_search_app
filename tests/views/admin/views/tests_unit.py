""" Unit tests for `core_federated_search_app.views.admin.views` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_federated_search_app.views.admin import views as admin_views
from core_main_app.commons.exceptions import NotUniqueError
from requests.exceptions import SSLError


class TestAddRepositoryGet(TestCase):
    """Unit tests for `add_repository` function for GET requests."""

    def setUp(self):
        """setUp"""
        mock_request = MagicMock()
        mock_request.method = "GET"
        self.mock_kwargs = {"request": mock_request}

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_repository_form_called(
        self, mock_admin_render, mock_repository_form
    ):
        """test_repository_form_called"""
        admin_views.add_repository(**self.mock_kwargs)
        mock_repository_form.assert_called_with()

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_admin_render_called(
        self, mock_admin_render, mock_repository_form
    ):
        """test_admin_render_called"""
        mock_repository_form_object = MagicMock()
        mock_repository_form.return_value = mock_repository_form_object

        admin_views.add_repository(**self.mock_kwargs)

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets={
                "js": [
                    {
                        "path": "core_federated_search_app/admin/js/repositories/add/form.js",
                        "is_raw": False,
                    },
                ],
                "css": ["core_federated_search_app/admin/css/add/form.css"],
            },
            context={"repository_form": mock_repository_form_object},
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_admin_render_returned(
        self, mock_admin_render, mock_repository_form
    ):
        """test_admin_render_returned"""
        expected_result = MagicMock()
        mock_admin_render.return_value = expected_result

        self.assertEqual(
            admin_views.add_repository(**self.mock_kwargs), expected_result
        )


class TestAddRepositoryPost(TestCase):
    """Unit tests for `add_repository` function for POST requests."""

    def setUp(self):
        """setUp"""
        mock_request = MagicMock()
        mock_request.method = "POST"
        self.mock_kwargs = {"request": mock_request}

        self.default_assets = {
            "js": [
                {
                    "path": "core_federated_search_app/admin/js/repositories/add/form.js",
                    "is_raw": False,
                },
            ],
            "css": ["core_federated_search_app/admin/css/add/form.css"],
        }

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_repository_form_called(
        self, mock_admin_render, mock_repository_form
    ):
        """test_repository_form_called"""
        admin_views.add_repository(**self.mock_kwargs)
        mock_repository_form.assert_called_with(
            self.mock_kwargs["request"].POST
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_form_is_valid_called(
        self, mock_admin_render, mock_repository_form
    ):
        """test_form_is_valid_called"""
        mock_form_object = MagicMock()
        mock_repository_form.return_value = mock_form_object

        admin_views.add_repository(**self.mock_kwargs)
        mock_form_object.is_valid.assert_called_with()

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_add_instance_called(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_add_instance_called"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        admin_views.add_repository(**self.mock_kwargs)
        mock_api_instance.add_instance.assert_called_with(
            mock_form_object.data["name"],
            mock_form_object.data["endpoint"],
            bool(mock_form_object.data.get("is_private_repo", None)),
            mock_form_object.data["client_id"],
            mock_form_object.data["client_secret"],
            mock_form_object.data["username"],
            mock_form_object.data["password"],
            mock_form_object.data["timeout"],
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "reverse")
    @patch.object(admin_views, "HttpResponseRedirect")
    def test_instance_not_none_reverse_called(
        self,
        mock_http_response_redirect,
        mock_reverse,
        mock_api_instance,
        mock_repository_form,
    ):
        """test_instance_not_none_reverse_called"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.return_value = MagicMock()

        admin_views.add_repository(**self.mock_kwargs)
        mock_reverse.assert_called_with(
            "core-admin:core_federated_search_app_repositories"
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "reverse")
    @patch.object(admin_views, "HttpResponseRedirect")
    def test_instance_not_none_http_response_redirect_called(
        self,
        mock_http_response_redirect,
        mock_reverse,
        mock_api_instance,
        mock_repository_form,
    ):
        """test_instance_none_http_response_redirect_called"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.return_value = MagicMock()

        mock_reverse_value = MagicMock()
        mock_reverse.return_value = mock_reverse_value

        admin_views.add_repository(**self.mock_kwargs)
        mock_http_response_redirect.assert_called_with(mock_reverse_value)

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "reverse")
    @patch.object(admin_views, "HttpResponseRedirect")
    def test_instance_none_http_response_redirect_returned(
        self,
        mock_http_response_redirect,
        mock_reverse,
        mock_api_instance,
        mock_repository_form,
    ):
        """test_instance_none_http_response_redirect_returned"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.return_value = MagicMock()

        mock_reverse_value = MagicMock()
        mock_reverse.return_value = mock_reverse_value

        expected_result = MagicMock()
        mock_http_response_redirect.return_value = expected_result

        self.assertEqual(
            admin_views.add_repository(**self.mock_kwargs), expected_result
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_add_instance_not_unique_error_adds_error_to_context(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_add_instance_not_unique_error_adds_error_to_context"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.side_effect = NotUniqueError(
            "mock_add_instance_not_unique_error"
        )

        admin_views.add_repository(**self.mock_kwargs)

        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets=self.default_assets,
            context={
                "repository_form": mock_form_object,
                "error": "An instance with the same parameters already exists.",
            },
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_add_instance_ssl_error_adds_error_to_context(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_add_instance_ssl_error_adds_error_to_context"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.side_effect = SSLError(
            "mock_add_instance_ssl_error"
        )

        admin_views.add_repository(**self.mock_kwargs)
        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets=self.default_assets,
            context={
                "repository_form": mock_form_object,
                "error": "Unable to reach the remote HTTPS instance.",
            },
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_add_instance_exception_adds_error_to_context(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_add_instance_exception_adds_error_to_context"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_exception = Exception("mock_add_instance_exception")
        mock_api_instance.add_instance.side_effect = mock_exception

        admin_views.add_repository(**self.mock_kwargs)
        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets=self.default_assets,
            context={
                "repository_form": mock_form_object,
                "error": str(mock_exception),
            },
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "admin_render")
    def test_form_is_invalid_adds_error_to_context(
        self, mock_admin_render, mock_repository_form
    ):
        """test_form_is_invalid_adds_error_to_context"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = False
        mock_repository_form.return_value = mock_form_object

        admin_views.add_repository(**self.mock_kwargs)
        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets=self.default_assets,
            context={
                "repository_form": mock_form_object,
                "error": "The form entered is not valid.",
            },
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_admin_render_called(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_admin_render_called"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.return_value = None

        admin_views.add_repository(**self.mock_kwargs)
        mock_admin_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_federated_search_app/admin/repositories/add_repository.html",
            assets=self.default_assets,
            context={"repository_form": mock_form_object},
            modals=None,
        )

    @patch.object(admin_views, "RepositoryForm")
    @patch.object(admin_views, "api_instance")
    @patch.object(admin_views, "admin_render")
    def test_admin_render_returned(
        self, mock_admin_render, mock_api_instance, mock_repository_form
    ):
        """test_admin_render_returned"""
        mock_form_object = MagicMock()
        mock_form_object.is_valid.return_value = True
        mock_repository_form.return_value = mock_form_object

        mock_api_instance.add_instance.return_value = None

        expected_result = MagicMock()
        mock_admin_render.return_value = expected_result

        self.assertEqual(
            admin_views.add_repository(**self.mock_kwargs), expected_result
        )
