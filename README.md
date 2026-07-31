# Shelf Manager

A small automation tool for managing manga releases.

Shelf Manager checks for new releases, downloads them, organizes the files, and prepares them for use with a Jellyfin library.

Currently configured for a single manga website, but plans to support more in the future.

## Features

* Scrapes release pages for new chapters
* Tracks downloaded releases with SQLite
* Downloads releases from MEGA
* Converts downloaded files into CBZ format
* Moves completed downloads into a Jellyfin library folder
* Supports environment-based configuration
* Sends notifications for new releases (optional)

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd shelf-manager
```

Install the project and dependencies:

```bash
pip install -e .
```

Create your environment file:

```bash
cp .env.example .env
```

Update `.env` with your paths and settings.

Example:

```env
RELEASE_URL="https://example.com/releases"
SERIES_TITLE="The JOJOLands"

DOWNLOAD_DIRECTORY="src/infrastructure/data/downloads"
DATABASE_DIRECTORY="src/infrastructure/data/database"

JELLYFIN_DIRECTORY="/path/to/jellyfin/library"

DISCORD_WEBHOOK_URL=""
```

## Running

Run the application from the project root:

```bash
python -m shelf_manager.main
```

The program will:

1. Initialize the database
2. Check for any existing downloads
3. Scan for new releases
4. Download new chapters
5. Move completed files into the Jellyfin directory
6. Update the database

## Database

The project uses SQLite to track downloaded releases.

The database stores:

* Series title
* Release type
* Chapter number
* MEGA URL
* Download status
* Download timestamp

## Configuration

All configurable values should be stored in `.env`.

Current configuration options:

| Variable              | Description                           |
| --------------------- | ------------------------------------- |
| `RELEASE_URL`         | Release page to scrape                |
| `SERIES_TITLE`        | Series name                           |
| `DOWNLOAD_DIRECTORY`  | Temporary download location           |
| `DATABASE_DIRECTORY`  | SQLite database location              |
| `JELLYFIN_DIRECTORY`  | Final CBZ storage location            |
| `DISCORD_WEBHOOK_URL` | Optional Discord notification webhook |

## Notes

This project is currently designed around a personal Jellyfin setup. Some paths and behaviors may need to be adjusted depending on your directory layout.
