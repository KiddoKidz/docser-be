from sys import maxsize
from uuid import uuid1

from meilisearch.errors import MeiliSearchApiError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .models import TOCHomepage
from .serializers import (
    FileLocationSearchSerializer,
    FileOwnerSearchSerializer,
    FileSearchSerializer,
    TOCDataSearchSerializer,
    TOCHomepageSerializer,
    TOCUploadSerializer,
)
from .utils import (
    build_facet_filters,
    build_filter_query,
    check_request_data_values_are_empty,
    get_meili_client,
    get_meili_search_error_response,
    processing_files_and_folders_toc,
)


class File(APIView):
    def post(self, request):
        is_request_data_values_empty = check_request_data_values_are_empty(
            request.data.values()
        )
        if is_request_data_values_empty:
            return Response(data={"error": False, "data": []})

        meili_client = get_meili_client()

        search_parameters = {
            "limit": 100,
            "attributesToCrop": ["content"],
            "attributesToHighlight": ["name", "content"],
            "cropLength": 50,
        }

        serializer = FileSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        filter_query = build_filter_query(
            serialized_data["start_time"],
            serialized_data["end_time"],
        )

        facet_filters = build_facet_filters(
            serialized_data["owners"],
            serialized_data["shared_by"],
            serialized_data["locations"],
            serialized_data["mime_types"],
        )

        if len(filter_query):
            search_parameters["filters"] = " AND ".join(filter_query)

        if len(facet_filters):
            search_parameters["facetFilters"] = facet_filters

        try:
            response = meili_client.index("files").search(
                serialized_data.get("q"), search_parameters
            )
        except MeiliSearchApiError as err:
            return get_meili_search_error_response(err)

        return Response(
            data={
                "error": False,
                "data": [res.get("_formatted", {}) for res in response.get("hits", [])],
            }
        )


class FileLocation(APIView):
    def post(self, request):
        meili_client = get_meili_client()

        search_parameters = {
            "limit": 10,
        }

        serializer = FileLocationSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        try:
            response = meili_client.index("file_locations").search(
                serialized_data.get("q"), search_parameters
            )
        except MeiliSearchApiError as err:
            return get_meili_search_error_response(err)

        return Response(
            data={
                "error": False,
                "data": response.get("hits", []),
            }
        )


class FileOwner(APIView):
    def post(self, request):
        meili_client = get_meili_client()

        search_parameters = {
            "limit": 10,
        }

        serializer = FileOwnerSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        try:
            response = meili_client.index("file_owners").search(
                serialized_data.get("q"), search_parameters
            )
        except MeiliSearchApiError as err:
            return get_meili_search_error_response(err)

        return Response(
            data={
                "error": False,
                "data": response.get("hits", []),
            }
        )


class TOCDataUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        # Setup primaryKey pakai apa? UUID
        # Cek admin atau bukan

        # if request.user.is_admin:
        toc_data_columns = 5

        uploaded_file = request.data.get("file", None)

        if not uploaded_file:
            return Response(
                data={"error": True, "file": "This field is required!"},
                status=HTTP_400_BAD_REQUEST,
            )

        file_data = uploaded_file.read().decode("utf-8")

        splitted_file_data_by_newline = file_data.split("\r\n")

        file_data_columns_title = splitted_file_data_by_newline.pop(0).split(",")
        if len(file_data_columns_title) != toc_data_columns:
            return Response(
                data={
                    "error": True,
                    "detail": "Failed to update TOC Data with "
                    + f"file {uploaded_file.name}. Invalid Data. "
                    + "Ensure you use the right template and fill in the "
                    + "required data.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        cleaned_data = []

        for row in splitted_file_data_by_newline:
            cols = row.split(",")
            if len(cols) != toc_data_columns:
                continue

            cleaned_data.append(
                {
                    "id": str(uuid1()),
                    "code": cols[0],
                    "name": cols[1],
                    "parents": [cols[2]] if cols[2] != "" else [],
                    "url": cols[3],
                    "type": str(cols[4]).lower(),
                }
            )

        processing_files_and_folders_toc(cleaned_data)

        return Response(
            data={
                "error": False,
                "detail": "TOC Data was successfully updated with "
                + f"file {uploaded_file.name}!",
            }
        )


class TOCDataTreeView(APIView):
    def get(self, request):
        meili_client = get_meili_client()
        response = meili_client.index("toc_data").get_documents({"limit": maxsize})

        childFolders = []
        childFiles = []
        rootFoldersWithoutCode = []
        rootFoldersWithCode = []
        rootFiles = []

        while len(response) > 0:
            current_data = response.pop()
            if current_data["type"] == "folder":
                if len(current_data["parents"]) == 0:
                    if current_data["code"] == "":
                        rootFoldersWithoutCode.append(current_data)
                    else:
                        rootFoldersWithCode.append(current_data)
                else:
                    childFolders.append(current_data)
            else:
                if len(current_data["parents"]) == 0:
                    rootFiles.append(current_data)
                else:
                    childFiles.append(current_data)

        return Response(
            data={
                "error": False,
                "data": {
                    "folders": {
                        "root": {
                            "withCode": rootFoldersWithCode,
                            "withoutCode": rootFoldersWithoutCode,
                        },
                        "child": childFolders,
                    },
                    "files": {"root": rootFiles, "child": childFiles},
                },
            }
        )


class TOCDataSearchView(APIView):
    def post(self, request):
        meili_client = get_meili_client()

        search_parameters = {"limit": 1000000000}

        serializer = TOCDataSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        if serialized_data.get("q"):
            search_parameters["limit"] = 10

        response = meili_client.index("toc_data").search(
            serialized_data.get("q"), search_parameters
        )
        return Response(data={"error": False, "data": response.get("hits", [])})


class TOCHomepageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        toc_homepage_columns = 10

        uploaded_file = request.data.get("file", None)
        if not uploaded_file:
            return Response(
                data={"error": True, "file": "This field is required!"},
                status=HTTP_400_BAD_REQUEST,
            )

        file_data = uploaded_file.read().decode("utf-8")

        splitted_file_data_by_newline = file_data.split("\r\n")

        file_data_columns_title = splitted_file_data_by_newline.pop(0).split(",")
        if len(file_data_columns_title) != toc_homepage_columns:
            return Response(
                data={
                    "error": True,
                    "detail": "Failed to update TOC Homepage with "
                    + f"file {uploaded_file.name}. Invalid Data. "
                    + "Ensure you use the right template and fill in the "
                    + "required data.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        for row in splitted_file_data_by_newline:
            cols = row.split(",")
            if len(cols) != toc_homepage_columns:
                continue
            toc_homepage = TOCHomepage.objects.get_or_create(id=cols[0])[0]
            toc_homepage.icon_url = cols[1]
            toc_homepage.category = cols[2]
            toc_homepage.description = cols[3]
            toc_homepage.data1_title = cols[4]
            toc_homepage.data1_url = cols[5]
            toc_homepage.data2_title = cols[6]
            toc_homepage.data2_url = cols[7]
            toc_homepage.data3_title = cols[8]
            toc_homepage.data3_url = cols[9]
            toc_homepage.save()

        return Response(
            data={
                "error": False,
                "detail": "TOC Homepage was successfully updated with "
                + f"file {uploaded_file.name}!",
            }
        )

    def get(self, request):
        toc_hompage_data = TOCHomepage.objects.all()
        serialized_data = TOCHomepageSerializer(toc_hompage_data, many=True).data
        return Response(data={"error": False, "data": serialized_data})
