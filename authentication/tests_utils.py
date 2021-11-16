import json
from unittest.mock import Mock


class FakeCredentials:
    token = "2dTdpEf9t43t5SxZKh4ArAUgAa7geqYWzijODJx5"
    refresh_token = "slY7fJRq6Wxu5AZ8KO4ufN3KkdL5vq4Bj6vQncSk"
    token_uri = "https://oauth2.googleapis.com/token"
    client_id = "p4OZ8B5n43X5PulC90AuyodKGAtQHElNRe5mceK4"
    client_secret = "ahuYHn1cfNFeugk1jQ5omNQL"
    scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.appdata",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.metadata",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/drive.photos.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
        "openid",
    ]


def get_fake_credentials():
    return {
        "token": "2dTdpEf9t43t5SxZKh4ArAUgAa7geqYWzijODJx5",
        "refresh_token": "slY7fJRq6Wxu5AZ8KO4ufN3KkdL5vq4Bj6vQncSk",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "p4OZ8B5n43X5PulC90AuyodKGAtQHElNRe5mceK4",
        "client_secret": "ahuYHn1cfNFeugk1jQ5omNQL",
        "scopes": [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.appdata",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.metadata",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/drive.photos.readonly",
            "https://www.googleapis.com/auth/drive.readonly",
            "openid",
        ],
    }


def get_fake_response_user_data(allowed_domain):
    email = "test_test@badak.com"
    if allowed_domain:
        email = "thunderbolts1412@gmail.com"
    return {
        "email": email,
        "given_name": "Test",
        "family_name": "User 1",
        "picture": "https://lh4.googleusercontent.com/",
    }


def get_oauth_request_get_mock(user_data):
    return Mock(
        text=json.dumps(user_data),
        ok=True,
    )
