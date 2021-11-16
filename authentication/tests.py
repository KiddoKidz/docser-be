import json
import re
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from google.oauth2.credentials import Credentials
from oauthlib.oauth2 import MismatchingStateError
from rest_framework.test import APITestCase

from .models import CustomUser, UserOAuth2Credentials
from .tests_utils import (
    FakeCredentials,
    get_fake_credentials,
    get_fake_response_user_data,
    get_oauth_request_get_mock,
)
from .utils import credentials_to_dict

# Create your tests here.


class UserModelTest(TestCase):
    def setUp(self):
        self.email = "dummy@sirclo.com"
        self.first_name = "Dummy"
        self.last_name = "Dummy"

        self.user = CustomUser.objects.create_user(self.email)
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

        self.admin_first_name = "admin"
        self.admin_last_name = "sirclo"
        self.admin_email = "admin@admin.com"

    def test_check_user(self):
        assert self.user.email == self.email
        assert self.user.first_name == self.first_name
        assert self.user.last_name == self.last_name
        self.assertEqual(self.user.is_staff, False)

    def test_create_super_user(self):
        admin_user = CustomUser.objects.create_superuser(self.admin_email)
        admin_user.first_name = self.admin_first_name
        admin_user.last_name = self.admin_last_name
        admin_user.save()

        assert admin_user.email == self.admin_email
        assert admin_user.first_name == self.admin_first_name
        assert admin_user.last_name == self.admin_last_name
        self.assertEqual(admin_user.is_staff, True)

    def test_has_perm_user(self):
        self.assertEqual(self.user.has_perm("authentication"), True)

    def test_has_module_perms_user(self):
        self.assertEqual(self.user.has_module_perms("authentication"), True)

    def test_user_string_repr(self):
        assert str(self.user) == self.email


class UserOAuth2CredentialsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="dummy@sirclo.com",
            first_name="Dummy",
            last_name="Dummy",
        )
        self.user.set_password(None)
        self.user.save()

        self.cred = UserOAuth2Credentials.objects.create(
            user=self.user,
            credentials=json.dumps(get_fake_credentials()),
        )

    def test_credential_string_repr(self):
        assert str(self.cred) == (str(self.user.email) + "Credentials")


class LoginViewTest(APITestCase):
    def test_login_as_user(self):
        response = self.client.get("/auth/login/", follow=False)
        assert response.status_code == 302
        assert re.match(
            r"https://accounts.google.com/o/oauth2/auth\?[\w\W\-\.:/\\]+", response.url
        )

    def test_login_as_admin(self):
        response = self.client.get("/auth/login/?is_admin=True", follow=False)
        assert response.status_code == 302
        assert re.match(
            r"https://accounts.google.com/o/oauth2/auth\?[\w\W\-\.:/\\]+", response.url
        )


class OAuth2CallbackViewTest(APITestCase):
    def setUp(self):
        get_patcher = patch("authentication.views.requests.get")
        flow_patcher = patch("authentication.views.Flow")
        update_files_to_meili_patcher = patch(
            "authentication.views.update_files_to_meili"
        )
        self.mock_flow = flow_patcher.start()
        self.mock_get = get_patcher.start()
        self.mock_update_files_to_meili = update_files_to_meili_patcher.start()

        self.mock_flow.from_client_secrets_file.return_value.credentials = (
            FakeCredentials()
        )

        self.mock_get.return_value = get_oauth_request_get_mock(
            get_fake_response_user_data(allowed_domain=True)
        )

        self.mock_update_files_to_meili.return_value.delay.return_value = ""

        self.addCleanup(self.mock_update_files_to_meili.stop)
        self.addCleanup(self.mock_flow.stop)
        self.addCleanup(self.mock_get.stop)

        self.session = self.client.session
        self.session["state"] = "12313123132131"
        self.session.save()

    def test_oauth2callback_success_as_user_with_update_files_to_meili(self):
        admin_user = CustomUser.objects.create_user("thunderbolts1412@gmail.com")
        admin_user.first_name = "Game"
        admin_user.last_name = "Mail"

        UserOAuth2Credentials.objects.create(
            user=admin_user, credentials=json.dumps(get_fake_credentials())
        )

        self.session["role"] = "user"
        self.session.save()

        response = self.client.get(
            "/auth/oauth2callback/",
            {
                "code": "4/0AY0e-g7NSwwbR4qq7ObwB6Ccw-p0MdlyzPbow-\
                    GBYW0NrqvlF0hJfB1u13QkwQd7si0ZGg",
            },
        )

        assert response.status_code == 302
        assert re.match(
            r"{0}\?token=[\w\W\-\.:/\\]+".format(settings.CORS_ALLOWED_ORIGINS[0]),
            response.url,
        )
        assert self.mock_flow.from_client_secrets_file.called
        assert self.mock_update_files_to_meili.delay.called

    def test_oauth2callback_success_as_user_without_update_files_to_meili(self):
        self.session["role"] = "user"
        self.session.save()

        response = self.client.get(
            "/auth/oauth2callback/",
            {
                "code": "4/0AY0e-g7NSwwbR4qq7ObwB6Ccw-p0MdlyzPbow-\
                    GBYW0NrqvlF0hJfB1u13QkwQd7si0ZGg",
            },
        )

        assert response.status_code == 302
        assert re.match(
            r"{0}\?token=[\w\W\-\.:/\\]+".format(settings.CORS_ALLOWED_ORIGINS[0]),
            response.url,
        )
        assert not self.mock_update_files_to_meili.delay.called

    def test_oauth2callback_success_as_admin_with_update_files_to_meili(self):
        self.session["role"] = "admin"
        self.session.save()

        response = self.client.get(
            "/auth/oauth2callback/",
            {
                "code": "4/0AY0e-g7NSwwbR4qq7ObwB6Ccw-p0MdlyzPbow-\
                    GBYW0NrqvlF0hJfB1u13QkwQd7si0ZGg",
            },
        )

        assert response.status_code == 302
        assert re.match(
            r"{0}\?token=[\w\W\-\.:/\\]+".format(settings.CORS_ALLOWED_ORIGINS[0]),
            response.url,
        )
        assert self.mock_flow.from_client_secrets_file.called
        assert self.mock_update_files_to_meili.delay.called

    def test_oauth2callback_domain_not_allowed(self):
        self.session["role"] = "user"
        self.session.save()

        self.mock_get.return_value = get_oauth_request_get_mock(
            get_fake_response_user_data(allowed_domain=False)
        )

        response = self.client.get(
            "/auth/oauth2callback/",
            {
                "code": "4/0AY0e-g7NSwwbR4qq7ObwB6Ccw-p0MdlyzPbow-\
                    GBYW0NrqvlF0hJfB1u13QkwQd7si0ZGg",
            },
        )

        assert response.status_code == 302
        assert re.match(r"{0}".format(settings.CORS_ALLOWED_ORIGINS[0]), response.url)

    def test_oauth2callback_state_mismatch_as_user(self):
        self.mock_flow.from_client_secrets_file.side_effect = MismatchingStateError

        self.session["role"] = "user"
        self.session.save()

        response = self.client.get(
            "/auth/oauth2callback/",
            {
                "code": "4/0AY0e-g7NSwwbR4qq7ObwB6Ccw-p0MdlyzPbow-\
                    GBYW0NrqvlF0hJfB1u13QkwQd7si0ZGg",
            },
        )

        assert response.status_code == 302
        assert re.match(r"{0}".format(settings.CORS_ALLOWED_ORIGINS[0]), response.url)


class UserInfoViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="dummy@sirclo.com",
            first_name="Dummy",
            last_name="Dummy",
            picture_url="https://lh4.googleusercontent.com/",
        )
        self.user.set_password(None)
        self.user.save()
        meilisearch_patcher = patch("api.utils.meilisearch")

        self.mock_meilisearch = meilisearch_patcher.start()

        self.mock_meilisearch.Client.return_value.get_keys.return_value = {
            "private": "aaaaa",
            "public": "aaaaa",
        }

        self.addCleanup(self.mock_meilisearch.stop)

    def test_get_user_info_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.get(
            "/auth/userinfo/",
        )

        assert response.status_code == 200

    def test_get_user_info_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "213123214jjr")
        response = self.client.get(
            "/auth/userinfo/",
        )
        assert response.status_code == 401


class UtilsTest(TestCase):
    def setUp(self):
        self.flow_credentials = Credentials(**get_fake_credentials())

    def test_credentials_to_dict(self):
        credentials_dict = credentials_to_dict(self.flow_credentials)
        assert len(credentials_dict.keys()) == 6
