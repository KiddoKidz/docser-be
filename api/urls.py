from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("drive/files/", views.File.as_view(), name="file"),
    path("drive/file_locations/", views.FileLocation.as_view(), name="file_location"),
    path("drive/file_owners/", views.FileOwner.as_view(), name="file_owner"),
    path("toc/data/upload/", views.TOCDataUploadView.as_view(), name="toc_data_upload"),
    path("toc/data/tree/", views.TOCDataTreeView.as_view(), name="toc_data_tree"),
    path("toc/data/search/", views.TOCDataSearchView.as_view(), name="toc_data_search"),
    path("toc/homepage/", views.TOCHomepageView.as_view(), name="toc_homepage"),
]
