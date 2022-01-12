from collections import namedtuple

from forwarder.formatter import GenericChannelFormatter
from forwarder.parser import MisterCoupon, SpaceCoupon

TECH_GROUP = -785446862  # Offerte Rubate - Tech
GENERIC_GROUP = -786771026  # Offerte Rubate - Generiche
HOME_GROUP = -652712250  # Offerte Rubate - Casa
FASHION_GROUP = -635115861  # Offerte Rubate - Moda
FPV_GROUP = -563703943  # Offerte Rubate (FPV)


ChannelSettings = namedtuple("ChannelSettings", ['destination_channel', "parser"])

CHANNELS_MAPPING = {
    "@mister_coupon": ChannelSettings(GENERIC_GROUP, MisterCoupon()),
    "@SpaceCoupon": ChannelSettings(GENERIC_GROUP, SpaceCoupon()),


    # "@MilkyWayShopping_Moda": FASHION_GROUP,
    # "@AlienSalesOfferte": FASHION_GROUP,
    #
    # "@fpvmattia": FPV_GROUP,
    # "@hardwareprogrammi": FPV_GROUP,
}

FORMATTERS = {
    GENERIC_GROUP: GenericChannelFormatter,
}