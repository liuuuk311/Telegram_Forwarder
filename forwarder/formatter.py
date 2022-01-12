import abc
import random
from typing import List

from forwarder.parser import ParsedDeal


class Formatter(abc.ABC):
    def __init__(self, parsed_deal: ParsedDeal):
        self.deal = parsed_deal

    @abc.abstractmethod
    def get_message_text(self) -> str:
        pass


class BasicDealFormatter(Formatter):
    title_emoji: str
    price_emoji: str
    urgency_messages: List[str]

    def format_urgency(self) -> str:
        if not self.urgency_messages:
            return ""
        return random.choice(self.urgency_messages)

    def format_title(self) -> str:
        return f"{self.title_emoji} **{self.deal.title}**"

    def format_price(self):
        if self.deal.old_price:
            return f"{self.price_emoji} PREZZO SCONTATO: **{self.deal.price}** al posto di {self.deal.old_price}"
        return f"{self.price_emoji} PREZZO: {self.deal.price}"

    def get_message_text(self) -> str:
        return f"""
            {self.format_urgency()}
            
            {self.format_title()}
            
            {self.format_price()} 
        """


class GenericChannelFormatter(BasicDealFormatter):
    title_emoji = "🎯"
    price_emoji = "💰"
