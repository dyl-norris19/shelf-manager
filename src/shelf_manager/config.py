import os
from dotenv import load_dotenv

load_dotenv()

RELEASE_URL = os.getenv("RELEASE_URL")
SERIES_TITLE = os.getenv("SERIES_TITLE")
DOWNLOAD_DIRECTORY = os.getenv(
    "DOWNLOAD_DIRECTORY",
    "src/infrastructure/data/downloads"
)
JELLYFIN_DIRECTORY = os.getenv(
    "JELLYFIN_DIRECTORY"
)
DATABASE_DIRECTORY = os.getenv(
    "DATABASE_DIRECTORY",
    "src/infrastructure/data/database"
)
DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)