from pathlib import Path
import shutil

from shelf_manager.config import JELLYFIN_DIRECTORY


JELLYFIN_PATH = Path(
    JELLYFIN_DIRECTORY
)


def move_to_jellyfin(file_path):
    """
    Move a completed CBZ file into the Jellyfin library.
    """

    source = Path(file_path)

    # Make sure the Jellyfin directory exists
    JELLYFIN_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = (
        JELLYFIN_PATH /
        source.name
    )

    if destination.exists():
        print(
            f"Already exists, skipping: {destination}"
        )

        source.unlink()

        return destination

    shutil.move(
        source,
        destination
    )

    destination.chmod(0o744)

    print(
        f"Moved to Jellyfin: {destination}"
    )

    return destination