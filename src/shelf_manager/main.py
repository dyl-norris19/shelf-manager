from shelf_manager.config import (
    RELEASE_URL,
    SERIES_TITLE
)

from scrapers.scraper import (
    get_page_html,
    find_chapters
)

from infrastructure.database import (
    initialize_database,
    release_exists,
    add_release
)

from infrastructure.downloader import (
    download_release,
    move_existing_downloads
)


def main():
    print(
        f"Checking {SERIES_TITLE} releases..."
    )

    print()

    try:
        initialize_database()

        move_existing_downloads()

        html = get_page_html(
            RELEASE_URL
        )

        releases = find_chapters(
            html
        )

        if not releases:
            print(
                "No releases found."
            )

            return

        new_releases = []

        for release in releases:

            chapter_number = release[
                "chapter"
            ]

            mega_url = release[
                "url"
            ]

            # Check database
            if release_exists(
                title=SERIES_TITLE,
                release_type="chapter",
                number=chapter_number
            ):
                continue

            print(
                "NEW RELEASE FOUND!"
            )

            print(
                f"Chapter {chapter_number}"
            )

            print(
                f"URL: {mega_url}"
            )

            print()

            # Download first
            download_successful = (
                download_release(
                    url=mega_url,
                    title=SERIES_TITLE,
                    release_type="chapter",
                    number=chapter_number
                )
            )

            # Only save to database if
            # download succeeded
            if download_successful:

                add_release(
                    title=SERIES_TITLE,
                    release_type="chapter",
                    number=chapter_number,
                    mega_url=mega_url
                )

                print(
                    "Release saved to database."
                )

                print()

            else:

                print(
                    "Release was NOT added "
                    "to the database."
                )

                print(
                    "It will be retried next time."
                )

                print()

    except Exception as error:

        print(
            f"An error occurred: {error}"
        )


if __name__ == "__main__":
    main()