import json

from django.conf import settings

from .models import CustomUser, UserOAuth2Credentials


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def create_or_update_user(user_data, user_credentials_dict, user_role):
    current_user, created = CustomUser.objects.get_or_create(email=user_data["email"])
    current_user.picture_url = user_data.get("picture", None)
    current_user.first_name = user_data.get("given_name", "")
    current_user.last_name = user_data.get("family_name", "")
    current_user.set_password(None)
    current_user.save()

    if current_user.email == settings.EMAIL_ADMIN and user_role == "admin":
        user_cred, created = UserOAuth2Credentials.objects.get_or_create(
            user=current_user,
        )
        user_cred.credentials = json.dumps(user_credentials_dict)
        user_cred.save()

    return current_user


def is_admin_credentials_exists():
    return UserOAuth2Credentials.objects.filter(
        user__email=settings.EMAIL_ADMIN
    ).exists()
