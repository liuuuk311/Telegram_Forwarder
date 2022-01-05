CHANNELS = {
    "SpaceCoupon": -1001489425802,
    "mister_coupon": -1001099842631,
    "MisterPrezzo": -1001478328942,
    "offerte_casa": -1001497307107,
    "Abbigliamento_Moda_Sconti": -1001446388912,
    "LaBottegaDelloSconto": -1001242443758,
    "Sconti_Offerte_H24": -1001454127828,
    "OutletPoint": -1001484762558,
    "AlienSalesOfferte": -1001151734636,
    "MilkyWayShopping_Moda": -1001272435575,
}

TECH_GROUP = 785446862  # Offerte Rubate - Tech
GENERIC_GROUP = 786771026  # Offerte Rubate - Generiche
HOME_GROUP = 652712250  # Offerte Rubate - Casa

FROM_TECH_CHATS = [
    -1001442610200,  # Robodeals
    -1001063843030,  # Offerte.tech
    -1001341651997,  # Offerte tecnologia
    -1001429891811,  # Tecno Offerte
]

FROM_HOME_CHATS = [
    CHANNELS["offerte_casa"]
]

FROM_GENERIC_CHATS = [
    CHANNELS["SpaceCoupon"],
    CHANNELS["mister_coupon"],
    CHANNELS["MisterPrezzo"],
    CHANNELS["AlienSalesOfferte"],
    CHANNELS["Sconti_Offerte_H24"],
    CHANNELS["LaBottegaDelloSconto"],
]