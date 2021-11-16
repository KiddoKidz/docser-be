import json
from unittest.mock import Mock


def get_meili_search_request_error_mock(
    error_message, error_code, error_link, status_code
):
    return Mock(
        text=json.dumps(
            {"message": error_message, "errorCode": error_code, "errorLink": error_link}
        ),
        status_code=status_code,
    )


def get_fake_files_changes_from_drive_api():
    return {
        "newStartPageToken": "51741",
        "changes": [
            {
                "changeType": "file",
                "removed": False,
                "fileId": "1dTtdjazJcztNAsNNHGX8cCyfL_wGxusRbN9j5Kk7Mok",
                "file": {
                    "id": "1dTtdjazJcztNAsNNHGX8cCyfL_wGxusRbN9j5Kk7Mok",
                    "name": "APA HAYOO??",
                    "mimeType": "application/vnd.google-apps.document",
                    "parents": ["0AFVyPfBRQstgUk9PVA"],
                    "webViewLink": "https://docs.google.com/document/d/1dTtdjazJcztNA",
                    "iconLink": "https://drive-thirdparty.googleusercontent.com/16/ty",
                    "createdTime": "2021-05-28T07:01:34.486Z",
                    "modifiedTime": "2021-05-28T07:01:54.627Z",
                    "owners": [
                        {
                            "kind": "drive#user",
                            "displayName": "Game Mail",
                            "me": True,
                            "permissionId": "16341377837335884107",
                            "emailAddress": "thunderbolts1412@gmail.com",
                        }
                    ],
                    "lastModifyingUser": {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    },
                    "shared": False,
                },
            },
            {
                "changeType": "file",
                "removed": False,
                "fileId": "1ouwzKho2DGIYEkvW2iXXwLts0CrHFvEbyKcXNOnb8zQ",
                "file": {
                    "id": "1ouwzKho2DGIYEkvW2iXXwLts0CrHFvEbyKcXNOnb8zQ",
                    "name": "Shrek pt 2",
                    "mimeType": "application/vnd.google-apps.document",
                    "parents": ["0AFVyPfBRQstgUk9PVA"],
                    "webViewLink": "https://docs.google.com/document/d/1ouwzKho2DGIYE",
                    "iconLink": "https://drive-thirdparty.googleusercontent.com/16/ty",
                    "createdTime": "2021-04-21T07:37:26.665Z",
                    "modifiedTime": "2021-04-21T07:37:45.846Z",
                    "owners": [
                        {
                            "kind": "drive#user",
                            "displayName": "Game Mail",
                            "me": True,
                            "permissionId": "16341377837335884107",
                            "emailAddress": "thunderbolts1412@gmail.com",
                        }
                    ],
                    "lastModifyingUser": {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    },
                    "shared": False,
                },
            },
            {
                "changeType": "file",
                "removed": True,
                "fileId": "1n6yKGoyRSwicP3SmNPYGIBlQXvy71jJ1Y_KVuih2b78",
            },
            {
                "changeType": "drive",
            },
        ],
    }


def get_fake_files_response_from_drive_api():
    return {
        "files": [
            {
                "id": "111111",
                "name": "Site Exmp",
                "mimeType": "application/vnd.google-apps.site",
                "parents": ["000000"],
                "webViewLink": "https://sites.google.com/s/111111/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-03T12:54:42.418Z",
                "modifiedTime": "2021-04-03T12:55:00.874Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "222222",
                "name": "Map Exmp",
                "mimeType": "application/vnd.google-apps.map",
                "parents": ["000000"],
                "webViewLink": "https://www.google.com/maps/d/edit?mid=222222",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-03T12:54:24.581Z",
                "modifiedTime": "2021-04-03T12:54:34.576Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "333333",
                "name": "Jam Exmp",
                "mimeType": "application/vnd.google-apps.jam",
                "parents": ["000000"],
                "webViewLink": "https://jamboard.google.com/d/333333/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-03T12:53:52.365Z",
                "modifiedTime": "2021-04-03T12:54:15.565Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "444444",
                "name": "Exmp Docs Shared",
                "mimeType": "application/vnd.google-apps.document",
                "webViewLink": "https://docs.google.com/document/d/444444/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2019-12-02T16:20:56.224Z",
                "modifiedTime": "2021-04-03T12:51:54.756Z",
                "sharingUser": {
                    "kind": "drive#user",
                    "displayName": "Lalalala User",
                    "me": False,
                    "permissionId": "12590993183994208414",
                    "emailAddress": "lalalala@gmail.com",
                },
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Lalalala User",
                        "me": False,
                        "permissionId": "12590993183994208414",
                        "emailAddress": "lalalala@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Lalalala User",
                    "me": False,
                    "permissionId": "12590993183994208414",
                    "emailAddress": "lalalala@gmail.com",
                },
                "shared": True,
            },
            {
                "id": "555555",
                "name": "The Pillow Book (1996)",
                "mimeType": "video/x-matroska",
                "parents": ["000000"],
                "webViewLink": "https://drive.google.com/file/d/555555/view",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2020-09-29T01:09:54.331Z",
                "modifiedTime": "2021-04-03T12:43:40.195Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": True,
            },
            {
                "id": "666666",
                "name": "PNG EXMP",
                "mimeType": "image/png",
                "parents": ["000000"],
                "webViewLink": "https://drive.google.com/file/d/666666/view",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-03T12:41:32.613Z",
                "modifiedTime": "2021-04-03T12:43:26.192Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "777777",
                "name": "PDF Exmp",
                "mimeType": "application/pdf",
                "parents": ["000000"],
                "webViewLink": "https://drive.google.com/file/d/777777/view",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T10:32:10.653Z",
                "modifiedTime": "2021-04-03T12:43:18.723Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "888888",
                "name": "Drawign Exmp",
                "mimeType": "application/vnd.google-apps.drawing",
                "parents": ["000000"],
                "webViewLink": "https://docs.google.com/drawings/d/888888/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T20:25:20.626Z",
                "modifiedTime": "2021-04-03T12:43:09.319Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "999999",
                "name": "Spreadsheet Exmp",
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": ["000000"],
                "webViewLink": "https://docs.google.com/spreadsheets/d/999999/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T10:20:32.172Z",
                "modifiedTime": "2021-04-03T12:42:57.658Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "010101",
                "name": "Slodes Exmp",
                "mimeType": "application/vnd.google-apps.presentation",
                "parents": ["000000"],
                "webViewLink": "https://docs.google.com/presentation/d/010101/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T10:36:05.138Z",
                "modifiedTime": "2021-04-03T12:42:48.257Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "020202",
                "name": "Form Exm",
                "mimeType": "application/vnd.google-apps.form",
                "parents": ["000000"],
                "webViewLink": "https://docs.google.com/forms/d/020202/edit",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-03T12:42:02.658Z",
                "modifiedTime": "2021-04-03T12:42:38.029Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "080808",
                "name": "test_dir_dir_08",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["050505"],
                "webViewLink": "https://drive.google.com/drive/folders/080808",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "090909",
                "name": "test_dir_09",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["000000"],
                "webViewLink": "https://drive.google.com/drive/folders/090909",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "030303",
                "name": "test_dir",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["090909"],
                "webViewLink": "https://drive.google.com/drive/folders/030303",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "040404",
                "name": "test_dir_dir_990",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["030303"],
                "webViewLink": "https://drive.google.com/drive/folders/040404",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "050505",
                "name": "test_dir_dir_995",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["030303"],
                "webViewLink": "https://drive.google.com/drive/folders/050505",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
            {
                "id": "060606",
                "name": "test_file_file_992",
                "mimeType": "application/vnd.google-apps.document",
                "parents": ["040404"],
                "webViewLink": "https://drive.google.com/document/060606",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": "2021-04-02T09:34:48.166Z",
                "modifiedTime": "2021-04-02T09:34:48.166Z",
                "owners": [
                    {
                        "kind": "drive#user",
                        "displayName": "Game Mail",
                        "me": True,
                        "permissionId": "16341377837335884107",
                        "emailAddress": "thunderbolts1412@gmail.com",
                    }
                ],
                "lastModifyingUser": {
                    "kind": "drive#user",
                    "displayName": "Game Mail",
                    "me": True,
                    "permissionId": "16341377837335884107",
                    "emailAddress": "thunderbolts1412@gmail.com",
                },
                "shared": False,
            },
        ]
    }


def get_fake_response_meili_file_search():
    return {
        "hits": [
            {
                "id": "0000",
                "name": "Getting started",
                "mimeType": "application/pdf",
                "webViewLink": "https://drive.google.com/eile/d/0000/view",
                "iconLink": "https://drive-thirdparty.googleusercontent.com/16/type",
                "createdTime": 1446987896072.0,
                "modifiedTime": 1446987896072.0,
                "owners": ["Game Mail"],
                "shared": False,
                "location": [],
                "lastModifedBy": "Game Mail",
                "content": "Store safely Sync seamlessly Add any ﬁle you  ",
                "sharedBy": "",
                "_formatted": {
                    "id": "0000",
                    "name": "<em>Getting</em> started",
                    "mimeType": "application/pdf",
                    "webViewLink": "https://drive.google.com/file/d/0000/view",
                    "iconLink": "https://drive-thirdparty.googleusercontent.com/16/ty",
                    "createdTime": 1446987896072.0,
                    "modifiedTime": 1446987896072.0,
                    "owners": ["Game Mail"],
                    "shared": False,
                    "location": [],
                    "lastModifedBy": "Game Mail",
                    "content": "Store safely Sync seamlessly Add any ﬁle you  ",
                    "sharedBy": "",
                },
            }
        ],
        "offset": 0,
        "limit": 100,
        "nbHits": 1,
        "exhaustiveNbHits": False,
        "processingTimeMs": 2,
        "query": "getting",
    }


def get_fake_response_meili_file_location_search():
    return {
        "hits": [
            {"id": "1_50d0d8dd11a959484cb8vASi205c14b2e51b64c68d", "name": "Shared"}
        ],
        "offset": 0,
        "limit": 100,
        "nbHits": 3,
        "exhaustiveNbHits": False,
        "processingTimeMs": 2,
        "query": "a",
    }


def get_fake_response_meili_file_owner_search():
    return {
        "hits": [
            {
                "id": "ab7d97a672c1e21e88082f48233eb8700a0ffc56",
                "name": "Hon Hui",
                "email": "Hon.hui@gmail.com",
            },
            {
                "id": "61ccec5a55a58016735cfc31245ba6af6c197445",
                "name": "Dania Driad",
                "email": "ddriad@gmail.com",
            },
            {
                "id": "175c0a063d39a2cd5b88851b15b44aedd89861bf",
                "name": "Kaia Kahn",
                "email": "kahn.kaian@gmail.com",
            },
        ],
        "offset": 0,
        "limit": 100,
        "nbHits": 3,
        "exhaustiveNbHits": False,
        "processingTimeMs": 2,
        "query": "gmail",
    }
