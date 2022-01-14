import logging
from typing import List, Optional

import requests
from telethon.tl.types import MessageEntityTextUrl, TypeMessageEntity
from bs4 import BeautifulSoup

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/83.0.4103.97 Safari/537.36 "


def extract_links(entities: Optional[List[TypeMessageEntity]]) -> List[str]:
    filtered = filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)
    return [x.url for x in filtered]


def is_amazon_link(url: str) -> bool:
    return url.startswith("https://www.amazon.it/") or url.startswith("https://amzn.to")


def get_amazon_image_from_page(url: str) -> str:
    headers = {'User-Agent': DEFAULT_USER_AGENT}
    response = requests.get(url, headers=headers, allow_redirects=True)
    if response.status_code != 200:
        logger.warning("Could not request the image from Amazon")
        return ""

    soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find("img", class_="a-dynamic-image")
    img_url = img.get("src", "")
    if not img_url:
        logger.warning(f"Could not get the image from Amazon page soup was {img}")

    return img_url

