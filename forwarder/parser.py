import abc
import re
from typing import List, Optional

from telethon.tl.types import Message, TypeMessageEntity

from forwarder.utils import extract_links


class ParsedDeal:
    price: str
    old_price: str
    title: str
    link: str

    def __init__(self, price, old_price, title, link):
        self.price = price
        self.old_price = old_price
        self.title = title
        self.link = link

    def __str__(self):
        return f"title: {self.title} price: {self.price} old: {self.old_price} link: {self.link}"


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
    def parse_link(self, entities: Optional[List[TypeMessageEntity]]) -> str:
        pass

    def parse(self, message: Message):
        return ParsedDeal(
            self.parse_price(message.message),
            self.parse_old_price(message.message),
            self.parse_title(message.message),
            self.parse_link(message.entities),
        )


class RegexParser(Parser):
    price_pattern: re.Pattern
    old_price_pattern: re.Pattern
    title_pattern: re.Pattern

    def parse_price(self, text: str) -> str:
        match = re.search(self.price_pattern, text)
        return match and match.group(0)

    def parse_old_price(self, text: str) -> str:
        match = re.search(self.old_price_pattern, text)
        return match and match.group(0)

    def parse_title(self, text: str) -> str:
        match = re.search(self.title_pattern, text)
        return match and match.group(0)

    @abc.abstractmethod
    def parse_link(self, entities: Optional[List[TypeMessageEntity]]) -> str:
        pass


class MisterCoupon(RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2})€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    title_pattern = re.compile(r"💥( [[:print:]]*)\n")

    def parse_link(self, entities: Optional[List[TypeMessageEntity]]) -> str:
        return entities and extract_links(entities)[0]
