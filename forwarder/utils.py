from typing import List

from telethon.tl.types import MessageEntityTextUrl


def extract_links(entities: List) -> List[str]:
    return list(map(lambda x: x.url, filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)))
