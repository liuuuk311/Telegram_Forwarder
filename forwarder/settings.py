from collections import namedtuple

from forwarder.formatter import GenericChannelFormatter
from forwarder.parser import SpaceCoupon, MilkyWayModa, AlienSales, OfferteModa, OfferteTech, Prodigeek, \
    OutletPoint, VideogiochiIT, BanggoodParser

TECH_GROUP = -785446862  # Offerte Rubate - Tech
GENERIC_GROUP = -786771026  # Offerte Rubate - Generiche
HOME_GROUP = -652712250  # Offerte Rubate - Casa
FASHION_GROUP = -635115861  # Offerte Rubate - Moda
FPV_GROUP = -563703943  # Offerte Rubate (FPV)


ChannelSettings = namedtuple("ChannelSettings", ['destination_channel', "parser"])

CHANNELS_MAPPING = {
    # "@mister_coupon": ChannelSettings(GENERIC_GROUP, MisterCoupon()),
    "@SpaceCoupon": ChannelSettings(GENERIC_GROUP, SpaceCoupon()),
    "@AlienSalesOfferte": ChannelSettings(GENERIC_GROUP, AlienSales()),

    "@offertepuntotech": ChannelSettings(TECH_GROUP, OfferteTech()),
    "@prodigeekOfferte": ChannelSettings(TECH_GROUP, Prodigeek()),
    "@videogiochi_it": ChannelSettings(TECH_GROUP, VideogiochiIT()),

    "@MilkyWayShopping_Moda": ChannelSettings(FASHION_GROUP, MilkyWayModa()),
    "@offertadelgiornomoda": ChannelSettings(FASHION_GROUP, OfferteModa()),
    "@OutletPoint": ChannelSettings(FASHION_GROUP, OutletPoint()),

    "@fpvmattia": ChannelSettings(FPV_GROUP, BanggoodParser()),
    "@hardwareprogrammi": ChannelSettings(FPV_GROUP, BanggoodParser()),
}

FORMATTERS = {
    GENERIC_GROUP: GenericChannelFormatter,
    FASHION_GROUP: GenericChannelFormatter,
    TECH_GROUP: GenericChannelFormatter,
}