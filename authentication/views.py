import copy
import json

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, reverse
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2 import OAuth2Error
from rest_framework import permissions, status
from rest_framework.authtoken.views import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.tasks import update_files_to_meili
from api.utils import get_meili_client, setup_meili_indexes

from .serializers import CustomUserSerializer
from .utils import (
    create_or_update_user,
    credentials_to_dict,
    is_admin_credentials_exists,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class LoginAuthToken(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        oauth2_scopes = copy.deepcopy(settings.GOOGLE_OAUTH2_SCOPES_DEFAULT)
        request.session["role"] = "user"

        if request.query_params.get("is_admin", False):
            oauth2_scopes.extend(settings.GOOGLE_OAUTH2_SCOPES_ADMIN_ONLY)
            request.session["role"] = "admin"

        flow = Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS,
            scopes=oauth2_scopes,
            redirect_uri=request.build_absolute_uri(
                reverse("authentication:oauth2callback")
            ),
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline", prompt="consent"
        )
        request.session["state"] = state

        return redirect(authorization_url)


class OAuth2Callback(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        redirect_url = settings.CORS_ALLOWED_ORIGINS[0]

        oauth2_scopes = copy.deepcopy(settings.GOOGLE_OAUTH2_SCOPES_DEFAULT)

        state = request.session["state"]
        if request.session["role"] == "admin":
            oauth2_scopes.extend(settings.GOOGLE_OAUTH2_SCOPES_ADMIN_ONLY)

        try:
            flow = Flow.from_client_secrets_file(
                settings.CLIENT_SECRETS,
                scopes=oauth2_scopes,
                redirect_uri=request.build_absolute_uri(
                    reverse("authentication:oauth2callback")
                ),
                state=state,
            )
        except OAuth2Error:
            return redirect(redirect_url)

        authorization_response = request.build_absolute_uri()

        if request.query_params.get("code", ""):
            flow.fetch_token(authorization_response=authorization_response)
            credentials_dict = credentials_to_dict(flow.credentials)
            request.session["credentials"] = credentials_dict

            res = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                {"alt": "json", "access_token": credentials_dict["token"]},
            )

            user_data = json.loads(res.text)

            email_domain = user_data["email"].split("@")[1]

            if email_domain in settings.ALLOWED_DOMAINS:
                current_user = create_or_update_user(
                    user_data, credentials_dict, request.session["role"]
                )

                meili_client = get_meili_client()
                setup_meili_indexes(meili_client)

                if (
                    current_user.email == settings.EMAIL_ADMIN
                    and is_admin_credentials_exists()
                ):
                    update_files_to_meili.delay()

                token, created = Token.objects.get_or_create(user=current_user)

                redirect_url = "{0}?token={1}".format(redirect_url, token)

        return redirect(redirect_url)


class UserInfo(APIView):
    def get(self, request, format=None):
        user_data = CustomUserSerializer(instance=request.user).data
        return Response(
            data={
                "email": user_data["email"],
                "full_name": "{0} {1}".format(
                    user_data["first_name"], user_data["last_name"]
                ),
                "picture_url": user_data["picture_url"],
            },
            status=status.HTTP_200_OK,
        )
