import logging
from typing import List, Optional

from telethon.tl.types import MessageEntityTextUrl, TypeMessageEntity

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")


def is_amazon_link(url: str) -> bool:
    return url.startswith("https://www.amazon.it/dp/") or url.startswith("https://amzn.to")


def extract_links(entities: Optional[List[TypeMessageEntity]]) -> List[str]:
    filtered = filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)
    return [x.url for x in filtered if is_amazon_link(x.url)]
