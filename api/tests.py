import json
from unittest.mock import patch

from django.core.cache import cache
from googleapiclient.discovery import HttpError
from meilisearch.errors import MeiliSearchApiError
from rest_framework.test import APITestCase

from authentication.models import CustomUser, UserOAuth2Credentials
from authentication.tests_utils import get_fake_credentials

from .tasks import update_files_changes_to_meili, update_files_to_meili
from .tests_utils import (
    get_fake_files_changes_from_drive_api,
    get_fake_files_response_from_drive_api,
    get_fake_response_meili_file_location_search,
    get_fake_response_meili_file_owner_search,
    get_fake_response_meili_file_search,
    get_meili_search_request_error_mock,
)
from .utils import get_meili_client


class FileViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="thunderbolts1412@gmail.com",
            first_name="Thunder",
            last_name="Dummy",
            picture_url="https://lh4.googleusercontent.com/",
        )
        self.user.set_password(None)
        self.user.save()

        get_meili_client_views_patcher = patch("api.views.get_meili_client")

        self.mock_get_meili_client_views = get_meili_client_views_patcher.start()

        self.mock_get_meili_client_views.return_value.index.return_value.search.return_value = (
            get_fake_response_meili_file_search()
        )

        self.addCleanup(self.mock_get_meili_client_views.stop)

    def test_search_file_from_meili_not_authorized(self):
        response = self.client.post("/api/drive/files/")

        assert response.status_code == 401

    def test_search_file_from_meili_not_giving_keyword(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
        )

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) == 0

    def test_search_file_from_meili_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post("/api/drive/files/", {"q": "getting"})

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_from_meili_with_filter_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "mime_types": ["application/pdf"],
                "start_time": 1619500000000,
                "end_time": 1619503942115,
                "owners": ["Game Mail"],
                "shared_by": ["Game Mail"],
                "locations": ["Shared", "My Drive"],
            },
        )

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_from_meili_with_filter_success_with_empty_request_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "",
                "mime_types": [],
                "owners": [],
                "shared_by": [],
                "locations": [],
            },
        )

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) == 0

    def test_search_file_from_meili_with_negative_start_time(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "start_time": -1619500000000,
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_search_file_from_meili_with_negative_end_time(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "end_time": -1619503942115,
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_search_file_from_meili_with_mime_types_contain_blank_string(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "mime_types": [""],
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_search_file_from_meili_with_owners_contain_blank_string(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "owners": [""],
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_search_file_from_meili_with_shared_by_contain_blank_string(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "shared_by": [""],
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_search_file_from_meili_with_locations_contain_blank_string(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
                "locations": ["", "My Drive"],
            },
        )

        assert response.status_code == 400
        assert response.data is not None

    def test_fail_search_file_using_filter(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        error_request_mock = get_meili_search_request_error_mock(
            "Error parsing filter",
            "invalid_filter",
            "https://docs.meilisearch.com/errors#invalid_filter",
            400,
        )
        self.mock_get_meili_client_views.return_value.index.return_value.search.side_effect = MeiliSearchApiError(
            "Error parsing filter", error_request_mock
        )

        response = self.client.post(
            "/api/drive/files/",
            {
                "q": "getting",
            },
        )

        assert response.status_code == 400
        assert response.data is not None


class FileLocationViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="thunderbolts1412@gmail.com",
            first_name="Thunder",
            last_name="Dummy",
            picture_url="https://lh4.googleusercontent.com/",
        )
        self.user.set_password(None)
        self.user.save()

        get_meili_client_views_patcher = patch("api.views.get_meili_client")

        self.mock_get_meili_client_views = get_meili_client_views_patcher.start()

        self.mock_get_meili_client_views.return_value.index.return_value.search.return_value = (
            get_fake_response_meili_file_location_search()
        )

        self.addCleanup(self.mock_get_meili_client_views.stop)

    def test_search_file_location_from_meili_not_authorized(self):
        response = self.client.post("/api/drive/file_locations/")

        assert response.status_code == 401

    def test_search_file_location_from_meili_not_giving_keyword(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/file_locations/",
        )

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_location_from_meili_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post("/api/drive/file_locations/", {"q": "getting"})

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_location_using_filter_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        error_request_mock = get_meili_search_request_error_mock(
            "Error parsing filter",
            "invalid_filter",
            "https://docs.meilisearch.com/errors#invalid_filter",
            400,
        )
        self.mock_get_meili_client_views.return_value.index.return_value.search.side_effect = MeiliSearchApiError(
            "Error parsing filter", error_request_mock
        )

        response = self.client.post(
            "/api/drive/file_locations/",
            {
                "q": "Shared",
            },
        )

        assert response.status_code == 400
        assert response.data is not None


class FileOwnerViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="thunderbolts1412@gmail.com",
            first_name="Thunder",
            last_name="Dummy",
            picture_url="https://lh4.googleusercontent.com/",
        )
        self.user.set_password(None)
        self.user.save()

        get_meili_client_views_patcher = patch("api.views.get_meili_client")

        self.mock_get_meili_client_views = get_meili_client_views_patcher.start()

        self.mock_get_meili_client_views.return_value.index.return_value.search.return_value = (
            get_fake_response_meili_file_owner_search()
        )

        self.addCleanup(self.mock_get_meili_client_views.stop)

    def test_search_file_owner_from_meili_not_authorized(self):
        response = self.client.post("/api/drive/file_owners/")

        assert response.status_code == 401

    def test_search_file_owner_from_meili_not_giving_keyword(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(
            "/api/drive/file_owners/",
        )

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_owner_from_meili_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post("/api/drive/file_owners/", {"q": "getting"})

        assert response.status_code == 200
        assert response.data is not None
        assert len(response.data["data"]) > 0

    def test_search_file_owner_using_filter_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        error_request_mock = get_meili_search_request_error_mock(
            "Error parsing filter",
            "invalid_filter",
            "https://docs.meilisearch.com/errors#invalid_filter",
            400,
        )
        self.mock_get_meili_client_views.return_value.index.return_value.search.side_effect = MeiliSearchApiError(
            "Error parsing filter", error_request_mock
        )

        response = self.client.post(
            "/api/drive/file_owners/",
            {
                "q": "gmail",
            },
        )

        assert response.status_code == 400
        assert response.data is not None


class ApiUtilTest(APITestCase):
    def setUp(self):
        meilisearch_utils_patcher = patch("api.utils.meilisearch")

        self.mock_meilisearch_utils = meilisearch_utils_patcher.start()

        self.addCleanup(self.mock_meilisearch_utils.stop)

    def test_get_meili_client(self):
        meili_client = get_meili_client()

        assert meili_client is not None


class ApiTaskTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="thunderbolts1412@gmail.com",
            first_name="Thunder",
            last_name="Dummy",
            picture_url="https://lh4.googleusercontent.com/",
        )
        self.user.set_password(None)
        self.user.save()

        self.cred = UserOAuth2Credentials.objects.create(
            user=self.user,
            credentials=json.dumps(get_fake_credentials()),
        )

        build_service_patcher = patch("api.tasks_utils.build")
        get_meili_client_tasks_patcher = patch("api.tasks_utils.get_meili_client")

        self.mock_build_service = build_service_patcher.start()
        self.mock_get_meili_client_tasks = get_meili_client_tasks_patcher.start()

        self.mock_build_service.return_value.files.return_value.export_media.return_value.execute.return_value = "Isi File".encode(
            "utf-8"
        )
        self.mock_build_service.return_value.files.return_value.list.return_value.execute.return_value = (
            get_fake_files_response_from_drive_api()
        )
        with open("./test_files/pdf_kosong.pdf", "rb") as pdf:
            self.mock_build_service.return_value.files.return_value.get_media.return_value.execute.return_value = (
                pdf.read()
            )

        self.mock_build_service.return_value.changes.return_value.list.return_value.execute.return_value = (
            get_fake_files_changes_from_drive_api()
        )

        self.mock_get_meili_client_tasks.return_value.index.return_value.search.return_value = (
            get_fake_response_meili_file_search()
        )
        meilisearch_utils_patcher = patch("api.utils.meilisearch")

        self.mock_meilisearch_utils = meilisearch_utils_patcher.start()

        self.addCleanup(self.mock_meilisearch_utils.stop)

        self.addCleanup(self.mock_build_service.stop)
        self.addCleanup(self.mock_get_meili_client_tasks.stop)

    def test_fetch_data_fail(self):
        self.mock_build_service.return_value.files.return_value.export_media.return_value.execute.side_effect = HttpError(
            "", b""
        )
        self.mock_build_service.return_value.files.return_value.get_media.return_value.execute.side_effect = HttpError(
            "", b""
        )

        update_files_to_meili()

        self.mock_build_service.assert_called()

    def test_update_files_to_meili(self):
        update_files_to_meili()

        self.mock_build_service.assert_called()

    def test_fetch_changes_fail(self):
        self.mock_build_service.return_value.changes.return_value.export_media.return_value.execute.side_effect = HttpError(
            "", b""
        )
        self.mock_build_service.return_value.changes.return_value.get_media.return_value.execute.side_effect = HttpError(
            "", b""
        )

        update_files_changes_to_meili()

        self.mock_build_service.assert_called()

    def test_fetch_changes_data(self):
        update_files_changes_to_meili()

        self.mock_build_service.assert_called()
