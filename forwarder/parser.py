import abc
import re
from abc import ABC
from typing import Optional

from telethon import TelegramClient

from forwarder.utils import extract_links, is_amazon_link


class ParsedDeal:
    price: str
    old_price: str
    title: str
    link: str
    image: str

    def __init__(self, price, old_price, title, link, image):
        self.price = price
        self.old_price = old_price
        self.title = title
        self.link = link
        self.image = image

    def __str__(self):
        return f"title: {self.title} price: {self.price} old: {self.old_price} link: {self.link} image: {self.image}"

    @property
    def is_valid(self):
        return self.title and self.price and self.link


class Parser(abc.ABC):
    client: TelegramClient

    @abc.abstractmethod
    def parse_price(self, text: str) -> str:
        pass

    @abc.abstractmethod
    def parse_old_price(self, text: str) -> str:
        pass

    @abc.abstractmethod
    def parse_title(self, text: str) -> str:
        pass

    @abc.abstractmethod
    def parse_link(self, link: str) -> str:
        pass

    @abc.abstractmethod
    def parse_image(self, link: str) -> str:
        pass

    @abc.abstractmethod
    async def get_price(self, event) -> str:
        pass

    @abc.abstractmethod
    async def get_old_price(self, event) -> str:
        pass

    @abc.abstractmethod
    async def get_title(self, event) -> str:
        pass

    @abc.abstractmethod
    async def get_link(self, event):
        pass

    @abc.abstractmethod
    async def get_image(self, event):
        pass

    async def parse(self, event):
        return ParsedDeal(
            self.parse_price(await self.get_price(event)),
            self.parse_old_price(await self.get_price(event)),
            self.parse_title(await self.get_title(event)),
            self.parse_link(await self.get_link(event)),
            self.parse_image(await self.get_image(event))
        )


class TextParser(Parser, ABC):
    async def get_price(self, event) -> str:
        return event.message.message

    async def get_old_price(self, event) -> str:
        return event.message.message

    async def get_title(self, event) -> str:
        return event.message.message


class RegexParser(TextParser, ABC):
    price_pattern: re.Pattern
    old_price_pattern: re.Pattern
    title_pattern: re.Pattern

    def parse_price(self, text: str) -> str:
        match = re.search(self.price_pattern, text)
        return match and match.group(1)

    def parse_old_price(self, text: str) -> str:
        match = re.search(self.old_price_pattern, text)
        return match and match.group(1)

    def parse_title(self, text: str) -> str:
        match = re.search(self.title_pattern, text)
        return match and match.group(1)


class AmazonLinkParserMixin:
    @staticmethod
    def parse_link(link: str) -> str:
        if is_amazon_link(link):
            return link
        return ""


class MisterCoupon(AmazonLinkParserMixin, RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2})€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    title_pattern = re.compile(r"💥 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")

    async def get_image(self, event) -> str:
        return event.media.webpage.url

    def parse_image(self, url: str) -> Optional[str]:
        if url.startswith("https://images.zbcdn.ovh/"):
            return url

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[1]


class SpaceCoupon(AmazonLinkParserMixin, RegexParser):
    price_pattern = re.compile(r"💰 (\d+(,\d{2}?)€)")
    old_price_pattern = re.compile(r"anziché (\d+(,\d{2})€)!")
    title_pattern = re.compile(r"🛒 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")

    async def get_image(self, event) -> str:
        await self.client.download_media(event.message.media)
        return "downloaded"

    def parse_image(self, url: str) -> Optional[str]:
        return url

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[0]

