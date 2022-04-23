from collections import namedtuple

from forwarder.formatter import GenericChannelFormatter
from forwarder.parser import OfferteTech, Prodigeek, VideogiochiIT, BanggoodParser

# TECH_GROUP = -785446862  # Offerte Rubate - Tech
# GENERIC_GROUP = -786771026  # Offerte Rubate - Generiche
# HOME_GROUP = -652712250  # Offerte Rubate - Casa
# FASHION_GROUP = -635115861  # Offerte Rubate - Moda
# FPV_GROUP = -563703943  # Offerte Rubate (FPV)



TECH_GROUP = "@offerte_tech_italia"  # Offerte Rubate - Tech
GENERIC_GROUP = "@offerte_e_sconti_amazon"  # Offerte Rubate - Generiche
HOME_GROUP = -652712250  # Offerte Rubate - Casa
FASHION_GROUP = "@offerte_moda_italia"  # Offerte Rubate - Moda
FPV_GROUP = "@fpv_coupons"  # Offerte Rubate (FPV)



ChannelSettings = namedtuple("ChannelSettings", ['destination_channel', "parser"])

CHANNELS_MAPPING = {

    "@offertepuntotech": ChannelSettings(TECH_GROUP, OfferteTech()),
    "@prodigeekOfferte": ChannelSettings(TECH_GROUP, Prodigeek()),
    "@videogiochi_it": ChannelSettings(TECH_GROUP, VideogiochiIT()),

    "@fpvmattia": ChannelSettings(FPV_GROUP, BanggoodParser()),
    "@hardwareprogrammi": ChannelSettings(FPV_GROUP, BanggoodParser()),
    "@RHobbyOfferte": ChannelSettings(FPV_GROUP, BanggoodParser()),
}

FORMATTERS = {
    GENERIC_GROUP: GenericChannelFormatter,
    FASHION_GROUP: GenericChannelFormatter,
    TECH_GROUP: GenericChannelFormatter,
    FPV_GROUP: GenericChannelFormatter,
}