import abc
import re
from abc import ABC
from typing import List, Optional

from telethon.tl.types import Message, TypeMessageEntity

from forwarder.utils import extract_amazon_links, extract_links


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
    def parse_link(self, entities: Optional[List]) -> str:
        pass

    @abc.abstractmethod
    def parse_image(self, entities: Optional[List]) -> str:
        pass

    def parse(self, event):
        return ParsedDeal(
            self.parse_price(event.message.message),
            self.parse_old_price(event.message.message),
            self.parse_title(event.message.message),
            self.parse_link(event.message.entities),
            self.parse_image(event.media.url)
        )


class RegexParser(Parser, ABC):
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
    def parse_link(entities: Optional[List[TypeMessageEntity]]) -> str:
        links = extract_amazon_links(entities)
        if len(links) > 0:
            return links[0]
        return ""


class MisterCoupon(AmazonLinkParserMixin, RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2})€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    title_pattern = re.compile(r"💥 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")

    def parse_image(self, entities: Optional[List]) -> str:
        links = extract_links(entities)
        for link in links:
            if link.startswith("https://images.zbcdn.ovh/"):
                return link
