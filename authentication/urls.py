from unicodedata import name
from django.urls import path

from . import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.LoginAuthToken.as_view(), name="login"),
    path("oauth2callback/", views.OAuth2Callback.as_view(), name="oauth2callback"),
    path("userinfo/", views.UserInfo.as_view(), name="userinfo"),
    path(
        "refresh-docser-data",
        views.RefreshDocSerData.as_view(),
        name="refresh_docser_data",
    ),
]
