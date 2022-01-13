import abc
import random
from typing import List

from forwarder.affiliate import overwrite_affiliate
from forwarder.images import create_our_image
from forwarder.parser import ParsedDeal


class Formatter(abc.ABC):
    def __init__(self, parsed_deal: ParsedDeal):
        self.deal = parsed_deal
        self._prepare_deal()

    def _prepare_deal(self):
        self.deal.link = overwrite_affiliate(self.deal.link)
        self.deal.image = create_our_image(self.deal.image)

    @abc.abstractmethod
    def get_message_text(self) -> str:
        pass


class BasicDealFormatter(Formatter):
    title_emoji: str
    price_emoji: str
    link_emoji: str
    urgency_messages: List[str] = []

    def format_urgency(self) -> str:
        if not self.urgency_messages:
            return ""
        return random.choice(self.urgency_messages)

    def format_title(self) -> str:
        return f"{self.title_emoji or ''} __{self.deal.title}__"

    def format_price(self):
        if self.deal.old_price:
            return f"{self.price_emoji or ''} PREZZO: **{self.deal.price}** al posto di {self.deal.old_price}"
        return f"{self.price_emoji or ''} PREZZO: {self.deal.price}"

    def format_link(self):
        return f"{self.link_emoji or ''} {self.deal.link}"

    def get_message_text(self) -> str:
        return f"{self.format_urgency()}\n\n{self.format_title()}\n\n{self.format_price()}\n\n{self.format_link()}"


class GenericChannelFormatter(BasicDealFormatter):
    title_emoji = "🎯"
    price_emoji = "💰"
    link_emoji = "🔗"
    urgency_messages = [
        "⏰ **OFFERTA A TEMPO LIMITATO** ⏰",
        "⚡️ **OFFERTA LAMPO** ⚡️",
        "💣 **PREZZO BOMBA** 💣",
        "🤯 **CHE OFFERTA** 🤯",
        "‼️ **DA NON FARSI SCAPPARE** ‼️",
        "⏳ **POCHI PEZZI DISPONIBILI** ⏳",
    ]