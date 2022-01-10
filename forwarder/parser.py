import abc
import re


class ParsedDeal:
    price: str
    old_price: str
    title: str

    def __init__(self, price, old_price, title):
        self.price = price
        self.old_price = old_price
        self.title = title


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

    def parse(self, message: str):
        return ParsedDeal(
            self.parse_price(message),
            self.parse_old_price(message),
            self.parse_title(message),
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


class MisterCoupon(RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2})€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    title_pattern = re.compile(r"💥( [[:print:]]*)\n")
