import logging
from typing import List

from telethon.tl.types import MessageEntityTextUrl
from telethon.utils import get_inner_text

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")


def extract_links(entities: List, text: str) -> List[str]:
    filtered = filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)
    return get_inner_text(text, filtered)
