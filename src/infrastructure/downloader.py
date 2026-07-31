from pathlib import Path
from mega import Mega

from shelf_manager.config import DOWNLOAD_DIRECTORY
from shelf_manager.notifications import send_notification


DOWNLOAD_PATH = Path(
    DOWNLOAD_DIRECTORY
)

from infrastructure.jellyfin import move_to_jellyfin


def move_existing_downloads():
    """
    Move any existing CBZ files from downloads
    into the Jellyfin library.
    """

    DOWNLOAD_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    cbz_files = list(
        DOWNLOAD_PATH.glob("*.cbz")
    )

    for file in cbz_files:
        print(
            f"Moving existing download: {file.name}"
        )

        move_to_jellyfin(file)


def clean_download_directory():
    """
    Remove all files from the downloads directory.
    """

    DOWNLOAD_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    for file in DOWNLOAD_PATH.iterdir():

        if file.is_file():
            file.unlink()


def download_release(
    url,
    title,
    release_type,
    number
):
    """
    Download a release from MEGA,
    rename the downloaded ZIP to a CBZ,
    and move it to Jellyfin dir.

    Returns:
        True  -> download succeeded
        False -> download failed
    """

    DOWNLOAD_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    try:
        # Remove old files first
        #most likely dead code: clean_download_directory()

        print(
            f"Downloading {title} "
            f"{release_type} {number}..."
        )

        mega = Mega()

        mega.download_url(
            url,
            dest_path=str(DOWNLOAD_PATH)
        )

        # Find the downloaded ZIP file
        zip_files = list(
            DOWNLOAD_PATH.glob("*.zip")
        )

        if not zip_files:
            print(
                "Download completed, but "
                "no ZIP file was found."
            )

            return False

        # We expect one downloaded ZIP
        downloaded_file = zip_files[0]

        # Rename ZIP -> CBZ
        new_filename = (
            f"Chapter {number}.cbz"
        )

        new_path = (
            DOWNLOAD_PATH /
            new_filename
        )

        downloaded_file.rename(
            new_path
        )

        print(
            f"Saved as: {new_filename}"
        )

        move_to_jellyfin(new_path)

        return True

    except Exception as error:

        print(
            f"Download failed: {error}"
        )

        send_notification(
        f"❌ Download failed\n"
        f"{title} {release_type} {number}\n"
        f"Error: {error}"
    )

        return False