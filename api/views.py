from meilisearch.errors import MeiliSearchApiError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    FileLocationSearchSerializer,
    FileOwnerSearchSerializer,
    FileSearchSerializer,
)
from .utils import (
    build_facet_filters,
    build_filter_query,
    check_request_data_values_are_empty,
    get_meili_client,
    get_meili_search_error_response,
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
