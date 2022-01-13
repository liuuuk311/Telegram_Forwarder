from collections import namedtuple

from forwarder.formatter import GenericChannelFormatter
from forwarder.parser import MisterCoupon, SpaceCoupon, MilkyWayModa, AlienSales

TECH_GROUP = -785446862  # Offerte Rubate - Tech
GENERIC_GROUP = -786771026  # Offerte Rubate - Generiche
HOME_GROUP = -652712250  # Offerte Rubate - Casa
FASHION_GROUP = -635115861  # Offerte Rubate - Moda
FPV_GROUP = -563703943  # Offerte Rubate (FPV)


ChannelSettings = namedtuple("ChannelSettings", ['destination_channel', "parser", "image_crop_factor"])

CHANNELS_MAPPING = {
    # "@mister_coupon": ChannelSettings(GENERIC_GROUP, MisterCoupon(), 234),
    "@SpaceCoupon": ChannelSettings(GENERIC_GROUP, SpaceCoupon(), 150),
    "@AlienSalesOfferte": ChannelSettings(GENERIC_GROUP, AlienSales(), 0),


    "@MilkyWayShopping_Moda": ChannelSettings(FASHION_GROUP, MilkyWayModa(), 0),
    #
    # "@fpvmattia": FPV_GROUP,
    # "@hardwareprogrammi": FPV_GROUP,
}

FORMATTERS = {
    GENERIC_GROUP: GenericChannelFormatter,
}