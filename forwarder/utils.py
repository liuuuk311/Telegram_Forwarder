import logging
from typing import List

from telethon.tl.types import MessageEntityTextUrl

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")


def extract_links(entities: List) -> List[str]:
    logger.info(entities)
    filtered = filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)
    logger.info(list(filtered))
    for e in filtered:
        logger.info(e.url)
    return list(map(lambda x: x.url, filtered))
