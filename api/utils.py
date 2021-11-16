import meilisearch
from django.conf import settings
from rest_framework.response import Response


def get_meili_search_error_response(error):
    return Response(
        data={
            "error": True,
            "data": error.message,
        },
        status=error.status_code,
    )


def check_request_data_values_are_empty(values):
    for val in values:
        if bool(val):
            return False
    return True


def get_meili_client():
    meili_client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)
    return meili_client


def setup_meili_indexes(meili_client):
    for index_name in settings.MEILI_DEFAULT_INDEXES:
        meili_client.get_or_create_index(index_name, {"primaryKey": "id"})

    meili_client.index("files").update_attributes_for_faceting(
        ["owners", "location", "mimeType", "sharedBy"]
    )
    meili_client.index("files").update_settings(
        {"searchableAttributes": ["name", "content"]}
    )


def build_filter_query(start_time, end_time):
    filter_query = []

    if start_time:
        filter_query.append("modifiedTime >= {0}".format(start_time))

    if end_time:
        filter_query.append("modifiedTime <= {0}".format(end_time))

    return filter_query


def build_facet_filters(owners, shared_by, locations, mime_types):
    facet_filters = []
    if len(owners):
        facet_filters.append(["owners:{0}".format(owner) for owner in owners])

    if len(shared_by):
        facet_filters.append(["sharedBy:{0}".format(sharer) for sharer in shared_by])

    if len(locations):
        facet_filters.append(
            ["location:{0}".format(location) for location in locations]
        )

    if len(mime_types):
        facet_filters.append(
            ["mimeType:{0}".format(mime_type) for mime_type in mime_types]
        )

    return facet_filters
