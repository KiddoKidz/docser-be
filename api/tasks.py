from authentication.utils import is_admin_credentials_exists
from be_docser.celery import app

from .tasks_utils import (
    fetch_changes_from_drive,
    fetch_files_and_folders_from_drive,
    get_drive_with_admin_credentials,
    processing_files_and_folders,
    seperate_removed_and_updated_files_and_folders,
)


@app.task
def update_files_to_meili():
    if is_admin_credentials_exists():
        drive = get_drive_with_admin_credentials()

        files_and_folders = fetch_files_and_folders_from_drive(drive)

        processing_files_and_folders(drive, files_and_folders)


@app.task
def update_files_changes_to_meili():
    if is_admin_credentials_exists():
        drive = get_drive_with_admin_credentials()

        changed_files_and_folders = fetch_changes_from_drive(drive)

        (
            removed_files_and_folders_id,
            updated_files_and_folders,
        ) = seperate_removed_and_updated_files_and_folders(changed_files_and_folders)

        processing_files_and_folders(
            drive, updated_files_and_folders, removed_files_and_folders_id
        )
