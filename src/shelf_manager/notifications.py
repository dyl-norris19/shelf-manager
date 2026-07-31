import requests

from shelf_manager.config import DISCORD_WEBHOOK_URL


def send_notification(message):
    if not DISCORD_WEBHOOK_URL:
        return

    payload = {
        "content": message
    }

    requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=10
    )