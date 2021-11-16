from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("drive/files/", views.File.as_view(), name="file"),
    path("drive/file_locations/", views.FileLocation.as_view(), name="file_location"),
    path("drive/file_owners/", views.FileOwner.as_view(), name="file_owner"),
]
