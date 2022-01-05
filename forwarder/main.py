import asyncio

from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events
import requests

api_id = 3052860
api_hash = "c309b7d34c3c15d0f0dac5b503711e9b"

# Uncomment when we need a new session key
# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     session_key = client.session.save()
#     print(session_key)
#     exit()

session_key = "1BJWap1sBu14bV-xpw4dDlhMCtl9k_drCaXGaxfNdWVlSoDE233J-i5CU1XvqgUZr4Yn7J1JNPLIPf62FrkamVj3EAJoX7A8jwFfubboK1iHTWI6cvcJwo1yzzZ-UvyM2DZh-_KeJTBwyamRuK36tSxBw2nN4T14BK_EIjMkUGsqKCJwf-7wB49XjyNZMHG9BkEvRlhHiel2k0pYHIzbFDwcDzhRmEadXYfwqI-9WZLCy2aI8eU_kHpMFS5V0UH0pduX55n8S_pj9I_VUSYw4WtRGnu0KosZdUQ1ar-XuQd6n3bnApWwh2gKOHrnbnSJXMwDF5r2zFxKXFFnGOddhq9hLoF8DSBM="

# url = "https://firebasestorage.googleapis.com/v0/b/test1-ba648.appspot.com/o/prod.session?alt=media&token=86f917cc-e2e3-4fd8-9dea-1af759b40174"
# r = requests.get(url, allow_redirects=True)
# open('login.session', 'wb').write(r.content)

FROM_CHATS = [
    -1001159240979,
    -1001196885168,
    -1001161672347,
    -1001339383475,
    -1001317129788,
    -1001148795974,
]

DEAL_GROUP = -563703943
DEV_GROUP = -405845918


client = TelegramClient(StringSession(session_key), api_id, api_hash)
client.start()
client.send_message("me", "Rubo le offerte con questo account")

allowed_to_send_amazon_tracking_command = [
    800707983,   # Testing Bot
]

tracking_bot_chats = [
    263273773,
]

TECH_GROUP = 785446862
GENERIC_GROUP = 786771026
HOME_GROUP = 652712250

FROM_TECH_CHATS = [
    -1001442610200,  # Robodeals
    -1001063843030,  # Offerte.tech
    -1001341651997,  # Offerte tecnologia
    -1001429891811,  # Tecno Offerte
]

FROM_HOME_CHATS = [
    -1001497307107,  # Offerte casa
    -1001325047421,  # Mister Offerte Casa
]

FROM_GENERIC_CHATS = [
    -1001353291777,  # Offerte Amazon italia
]


@client.on(events.NewMessage(chats=FROM_CHATS))
@client.on(events.MessageEdited(chats=FROM_CHATS))
async def handler(event):
    to_chat = await client.get_entity(DEAL_GROUP)
    await event.message.forward_to(to_chat)


@client.on(
    events.NewMessage(
        pattern=r"get_ids",
    )
)
async def get_ids(event):
    channels = [
        "t.me/offerte_casa",
        "t.me/Abbigliamento_Moda_Sconti",
        "t.me/LaBottegaDelloSconto",
        "t.me/Sconti_Offerte_H24",
        "t.me/OutletPoint",
        "t.me/AlienSalesOfferte",
        "t.me/MilkyWayShopping_Moda",
        "t.me/SpaceCoupon",
        "t.me/mister_coupon",
        "t.me/MisterPrezzo",
    ]
    for channel in channels:
        print(f"{channel} -> {await client.get_entity(channel)}")


@client.on(
    events.NewMessage(
        chats=allowed_to_send_amazon_tracking_command,
        pattern=r"https:\/\/(www.)?(amazon\.it|amzn\.to)\/(\w*-?\/?\??=?&?)*",
    )
)
async def amazon_tracker_forward_handler(event):
    test = await client.get_entity("t.me/traccia_prezzo_bot")
    await event.message.forward_to(test)


# Remove comments if using IZ2ZUZ_BOT, but we'll need to figure out how to track different products
# @client.on(
#     events.NewMessage(
#         chats=tracking_bot_chats,
#     )
# )
# async def iz2zuz_forward_handler(event):
#     await event.message.forward_to(IZ2ZUZ_BOT)


@client.on(events.NewMessage(from_users=FROM_TECH_CHATS))
async def handler(event):
    await event.message.forward_to(TECH_GROUP)


@client.on(events.NewMessage(from_users=FROM_HOME_CHATS))
async def handler(event):
    await event.message.forward_to(HOME_GROUP)


@client.on(events.NewMessage(from_users=FROM_GENERIC_CHATS))
async def handler(event):
    await event.message.forward_to(GENERIC_GROUP)


client.run_until_disconnected()
