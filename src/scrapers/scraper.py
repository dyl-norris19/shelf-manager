# scraper.py

import re

import requests
from bs4 import BeautifulSoup


def get_page_html(url):
    """
    Download the release archive webpage and return its HTML.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def find_chapters(html):
    """
    Parse the webpage HTML and find all uncollected chapter releases.

    Returns a list of dictionaries containing:
        - chapter number
        - Mega download URL
    """

    soup = BeautifulSoup(html, "html.parser")

    chapters = []

    # Find the text "Uncollected Magazine Chapters"
    heading = soup.find(
        string=re.compile(
            r"Uncollected Magazine Chapters",
            re.IGNORECASE
        )
    )

    if heading is None:
        raise RuntimeError(
            "Could not find 'Uncollected Magazine Chapters' "
            "on the page."
        )

    # The heading is inside the same download-item container
    # as the chapter links.
    download_item = heading.find_parent(
        class_="download-item"
    )

    if download_item is None:
        raise RuntimeError(
            "Found the chapter heading, but could not find "
            "its download-item container."
        )

    # Find all links inside this section.
    links = download_item.find_all("a", href=True)

    for link in links:
        link_text = link.get_text(strip=True)

        # Look for text like:
        # Chapter 33
        # Chapter 34
        # Chapter 35
        match = re.fullmatch(
            r"Chapter\s+(\d+)",
            link_text,
            re.IGNORECASE
        )

        if not match:
            continue

        chapter_number = int(match.group(1))
        mega_url = link["href"]

        chapters.append({
            "chapter": chapter_number,
            "url": mega_url
        })

    # Sort from oldest chapter to newest chapter
    chapters.sort(
        key=lambda chapter: chapter["chapter"]
    )

    return chapters


def get_latest_chapter(html):
    """
    Return the newest chapter number found on the page.
    """

    chapters = find_chapters(html)

    if not chapters:
        raise RuntimeError(
            "No chapters were found."
        )

    return chapters[-1]


def get_new_chapters(html, latest_known_chapter):
    """
    Return all chapters newer than latest_known_chapter.
    """

    chapters = find_chapters(html)

    new_chapters = [
        chapter
        for chapter in chapters
        if chapter["chapter"] > latest_known_chapter
    ]

    return new_chapters