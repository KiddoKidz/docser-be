import meilisearch
from django.conf import settings
from rest_framework.response import Response

# Utils for document search feature


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

    meili_client.index("toc_data").update_settings({"searchableAttributes": ["name"]})


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


# Utils for ToC feature
def seperate_files_and_folders_toc(files_and_folders):
    folders = []
    files = []

    while len(files_and_folders) > 0:
        current_data = files_and_folders.pop()
        if current_data["type"] == "folder":
            folders.append(current_data)
        else:
            files.append(current_data)

    return files, folders


def update_current_folder_data_toc(current_folder, parent_folder):
    parent_folder_name = parent_folder["name"]

    current_folder["location"].extend(
        [parent_folder_name] + parent_folder.get("location", [])
    )

    current_folder["locationLink"][parent_folder_name] = parent_folder["url"]

    for name, link in parent_folder.get("locationLink", {}).items():
        current_folder["locationLink"][name] = link

    current_folder["parents"].extend(parent_folder["parents"])


def cleaning_folders_data_toc(folders):
    for current_folder in folders:
        current_folder["location"] = []
        current_folder["locationLink"] = {}

        i = len(current_folder.get("parents", [])) - 1
        current_total_parents = len(current_folder.get("parents", []))

        while (i < current_total_parents) & (i >= 0):
            for folder in folders:
                if folder["code"] == current_folder["parents"][i]:
                    update_current_folder_data_toc(current_folder, folder)
                    i += len(folder["parents"])

            if current_total_parents == len(current_folder["parents"]):
                break

            current_total_parents = len(current_folder["parents"])

    for current_folder in folders:
        current_folder["location"] = current_folder["location"][::-1]
        current_folder["parents"] = current_folder["parents"][::-1]


def cleaning_files_data_toc(folders, files):
    for file in files:

        file["location"] = []
        file["locationLink"] = {}

        for folder in folders:
            if len(file.get("parents", [])) and (folder["id"] == file["parents"][0]):
                parent_folder_name = folder["name"]
                file["location"].extend(folder["location"] + [parent_folder_name])
                file["locationLink"].update(folder["locationLink"])
                file["locationLink"][parent_folder_name] = folder["url"]


def sync_to_meili_toc(cleaned_files, cleaned_folders):
    meili_client = get_meili_client()

    meili_client.index("toc_data").delete_all_documents()
    meili_client.index("toc_data").add_documents(cleaned_files)
    meili_client.index("toc_data").add_documents(cleaned_folders)


def processing_files_and_folders_toc(files_and_folders):
    files, folders = seperate_files_and_folders_toc(files_and_folders)

    cleaning_folders_data_toc(folders)
    cleaning_files_data_toc(folders, files)

    sync_to_meili_toc(files, folders)
