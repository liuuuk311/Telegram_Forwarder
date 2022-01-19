import logging
import random
from functools import lru_cache
from typing import List, Optional

import requests
from lxml.html import fromstring
from telethon.tl.types import MessageEntityTextUrl, TypeMessageEntity
from bs4 import BeautifulSoup


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")


@lru_cache
def get_proxies():
    response = requests.get('https://www.sslproxies.org/')
    parser = fromstring(response.text)
    return {
        f"https://{row.xpath('.//td[1]/text()')[0]}:{row.xpath('.//td[2]/text()')[0]}"
        for row in parser.xpath('//tbody/tr')[:15]
    }


def select_random_proxy():
    proxy = random.choice(list(get_proxies()))
    return {"http": proxy}


def extract_links(entities: Optional[List[TypeMessageEntity]]) -> List[str]:
    filtered = filter(lambda x: isinstance(x, MessageEntityTextUrl), entities)
    return [x.url for x in filtered]


def is_amazon_link(url: str) -> bool:
    return url.startswith("https://www.amazon.it/") or url.startswith("https://amzn.to")


def get_amazon_image_from_page(url: str) -> str:
    headers = {'User-Agent': get_random_user_agent(), 'Accept-Language': 'it-IT'}
    proxies = select_random_proxy()
    cookies = {
        'i18n-prefs': 'EUR',
        'session-id': '257-4568920-4927623',
        'session-token': 'ErsXvPHdc9wzTr8J/nJl7j4qct+LwljBEpcXoG+5GIwPcWzjqBjSCjnv5Og9Vf3PGPtn2V/YmkPSqRPCV96tpXGwDPCqq73ALIsrtyfq2WuWZj9jUF2RbYdj6PkBTbwrXPRADTAJyK5X+6g76cLgrwcfbpDTU4dqHHJnpDODHjqYJ8opAdmQD9xOJRb1mHUL',
        'ubid-acbit': '258-4147140-0370608',
        'csm-hit': 'tb:42MCAT6J68FH53DB7H4H+s-50HZ2JX85Q901CGKTEE8|1642166515597&t:1642166515597&adb:adblk_no',
        'session-id-time': '2082787201l'
    }
    response = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies, proxies=proxies)
    if response.status_code != 200:
        logger.warning("Could not request the image from Amazon")
        return ""

    soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find("img", class_="a-dynamic-image")
    if not img:
        logger.warning("Amazon page thinks we are a BOT, no content found!")
        return ""

    img_url = img.get("src", "")
    if not img_url:
        logger.warning(f"Could not get the image from Amazon page soup was {img}")

    return img_url


def get_random_user_agent():
    return random.choice([
        "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    ])
