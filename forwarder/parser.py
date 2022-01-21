import abc
import re
from abc import ABC
from typing import Optional, List

from telethon import TelegramClient
from telethon.tl.types import MessageEntityItalic
from telethon.utils import get_inner_text

from forwarder.affiliate import overwrite_affiliate
from forwarder.images import create_our_image, download_image
from forwarder.utils import extract_links, is_amazon_link, get_amazon_image_from_page, get_banggood_data, is_bg_link


class ParsedDeal:
    price: str
    old_price: str
    title: str
    link: str
    image: str

    mandatory_fields: List = ["price", "title", "link", "image"]

    def __init__(self, price, old_price, title, link, image):
        self.price = price
        self.old_price = old_price
        self.title = title
        self.link = link
        self.image = image

    def __str__(self):
        return f"title: {self.title} price: {self.price} old: {self.old_price} link: {self.link} image: {self.image}"

    @property
    def is_valid(self) -> bool:
        return all(getattr(self, field) for field in self.mandatory_fields)
        # return self.title and self.price and self.link and self.image

    @property
    def reason_not_valid(self) -> Optional[str]:
        missing_fields = [field for field in self.mandatory_fields if not getattr(self, field)]
        if not missing_fields:
            return
        return f"This deal is not valid because {missing_fields} are missing"


class Parser(abc.ABC):
    client: TelegramClient

    async def prepare_data(self, event):
        pass

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
        await self.prepare_data(event)
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
    old_price_pattern: Optional[re.Pattern]
    title_pattern: re.Pattern

    def parse_price(self, text: str) -> str:
        match = re.search(self.price_pattern, text)
        return match and match.group(1)

    def parse_old_price(self, text: str) -> str:
        if not self.old_price_pattern:
            return ""
        match = re.search(self.old_price_pattern, text)
        return match and match.group(1)

    def parse_title(self, text: str) -> str:
        match = re.search(self.title_pattern, text)
        return match and match.group(1)


class ImageCreatorMixin(Parser, ABC):
    template_name: str = "template.png"

    async def get_image_url(self, event) -> str:
        return get_amazon_image_from_page(await self.get_link(event))

    async def get_image(self, event) -> str:
        url = await self.get_image_url(event)
        if not url:
            return ""
        return create_our_image(
            download_image(url),
            template_name=self.template_name,
            price=self.parse_price(await self.get_price(event)),
            old_price=self.parse_old_price(await self.get_price(event)),
        )

    def parse_image(self, url: str) -> Optional[str]:
        return url


class AmazonLinkParserMixin:
    @staticmethod
    def parse_link(link: str) -> str:
        if is_amazon_link(link):
            return overwrite_affiliate(link)
        return ""


class MisterCoupon(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2})€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    title_pattern = re.compile(r"💥 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[1]


class SpaceCoupon(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"💰 (\d+(,\d{2}?)€)")
    old_price_pattern = re.compile(r"anziché (\d+(,\d{2})€)!")
    title_pattern = re.compile(r"🛒 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")
    template_name = "generic_template.jpeg"

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[0]


class MilkyWayModa(SpaceCoupon):
    template_name = "fashion_template.jpeg"


class AlienSales(SpaceCoupon):
    pass


class OfferteModa(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"a soli (\d+(,\d{2}?)€)")
    old_price_pattern = re.compile(r"da (\d+(,\d{2})€)")
    template_name = "fashion_template.jpeg"

    def parse_title(self, text: str) -> str:
        return text.split("\n")[0]

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[0]


class OutletPoint(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"💰 (\d+(,\d{2}?)€)")
    old_price_pattern = re.compile(r"anziché (\d+(,\d{2})€)")
    amazon_link_pattern = re.compile(r"((https?:\/\/)?(amzn\.to)\/\w*)")
    template_name = "fashion_template.jpeg"

    async def get_title(self, event) -> str:
        filtered = filter(lambda x: isinstance(x, MessageEntityItalic), event.message.entities)
        res = get_inner_text(event.message.message, filtered)
        return res if not isinstance(res, list) else res[0]

    def parse_title(self, text: str) -> str:
        return text

    async def get_link(self, event) -> str:
        match = re.search(self.amazon_link_pattern, event.message.message)
        return match and match.group(1)


class OfferteTech(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"💶 (\d+(,\d{2}?)€)")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2})€)")
    template_name = "tech_template.jpeg"

    def parse_title(self, text: str) -> str:
        return text.split("\n")[0]

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[1]


class Prodigeek(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"💰 Prezzo: (\d+(,\d{2}?)€)")
    old_price_pattern = None
    template_name = "tech_template.jpeg"

    def parse_title(self, text: str) -> str:
        return text.split("\n")[0]

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[1]


class VideogiochiIT(AmazonLinkParserMixin, ImageCreatorMixin, RegexParser):
    price_pattern = re.compile(r"⚡️(\d+(,\d{2}?)€)⚡️")
    old_price_pattern = re.compile(r"invece di (\d+(,\d{2}?)€)")
    template_name = "tech_template.jpeg"
    title_pattern = re.compile(r"💥 ((\w*\'?\'? ?,?\(?\)?-?\.?\/?%?\d?)*)\n")

    async def get_link(self, event) -> str:
        return extract_links(event.message.entities)[1]


class BanggoodParser(ImageCreatorMixin):
    scraped_data: dict
    template_name = "fpv_template.jpeg"
    link_pattern = re.compile(
        r"(?P<url>https?:\/\/[^\s]+)|((https?:\/\/)?((bit\.ly)|(banggood\.app\.link)|(m\.banggood\.com)|(amzn\.to))\/\w*)"
    )

    async def prepare_data(self, event):
        self.scraped_data = get_banggood_data(self.parse_link(await self.get_link(event)))

    async def get_image_url(self, event) -> str:
        return self.scraped_data.get("image")

    def parse_price(self, text: str) -> str:
        return text

    def parse_old_price(self, text: str) -> str:
        return text

    def parse_title(self, text: str) -> str:
        return text

    def parse_link(self, link: str) -> str:
        if is_bg_link(link):
            return overwrite_affiliate(link)

    async def get_price(self, event) -> str:
        return self.scraped_data.get("price")

    async def get_old_price(self, event) -> str:
        return self.scraped_data.get("old_price")

    async def get_title(self, event) -> str:
        return self.scraped_data.get("title")

    async def get_link(self, event):
        match = re.search(self.link_pattern, event.message.message)
        return match and match.group(1)


