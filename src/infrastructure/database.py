import sqlite3
from pathlib import Path

from shelf_manager.config import DATABASE_DIRECTORY


DATABASE_FILE = Path(DATABASE_DIRECTORY) / "releases.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    """
    Create the releases table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            number INTEGER NOT NULL,
            mega_url TEXT NOT NULL,
            downloaded INTEGER NOT NULL DEFAULT 0,
            downloaded_at TEXT,

            UNIQUE(title, type, number)
        )
    """)

    connection.commit()
    connection.close()


def release_exists(title, release_type, number):
    """
    Check if a release already exists in the database.

    Returns:
        True  -> release exists
        False -> release does not exist
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM releases
        WHERE title = ?
        AND type = ?
        AND number = ?
    """, (
        title,
        release_type,
        number
    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None


def add_release(
    title,
    release_type,
    number,
    mega_url
):
    """
    Add a new release to the database.

    Returns:
        True  -> release was added
        False -> release already existed
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO releases (
                title,
                type,
                number,
                mega_url
            )
            VALUES (?, ?, ?, ?)
        """, (
            title,
            release_type,
            number,
            mega_url
        ))

        connection.commit()

        return True

    except sqlite3.IntegrityError:
        # The UNIQUE constraint means this release
        # already exists in the database.
        return False

    finally:
        connection.close()


def get_all_releases(title=None):
    """
    Return all releases.

    If a title is provided, only return releases
    belonging to that series.
    """

    connection = get_connection()

    cursor = connection.cursor()

    if title:
        cursor.execute("""
            SELECT
                id,
                title,
                type,
                number,
                mega_url,
                downloaded,
                downloaded_at
            FROM releases
            WHERE title = ?
            ORDER BY number ASC
        """, (title,))

    else:
        cursor.execute("""
            SELECT
                id,
                title,
                type,
                number,
                mega_url,
                downloaded,
                downloaded_at
            FROM releases
            ORDER BY title ASC, number ASC
        """)

    releases = cursor.fetchall()

    connection.close()

    return releases