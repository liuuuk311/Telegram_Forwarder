import asyncio
import logging

from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events
import requests

from forwarder.parser import MisterCoupon
from forwarder.settings import CHANNELS_MAPPING
from forwarder.utils import extract_links

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")

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


client = TelegramClient(StringSession(session_key), api_id, api_hash)
client.start()
MAPPINGS = {}

# @client.on(
#     events.NewMessage(
#         chats=allowed_to_send_amazon_tracking_command,
#         pattern=r"https:\/\/(www.)?(amazon\.it|amzn\.to)\/(\w*-?\/?\??=?&?)*",
#     )
# )
# async def amazon_tracker_forward_handler(event):
#     to_chat = await client.get_entity("t.me/traccia_prezzo_bot")
#     await event.message.forward_to(to_chat)


async def build_id_mappings():
    for channel, group in CHANNELS_MAPPING.items():
        entity = await client.get_entity(channel)
        peer_id = await client.get_peer_id(entity)
        MAPPINGS[peer_id] = group

    logger.info(MAPPINGS)

parser = MisterCoupon()

@client.on(events.NewMessage)
async def generic_handler(event: events.NewMessage.Event):
    to_chat = MAPPINGS.get(event.chat_id)

    if to_chat:
        logger.info(f"Parsed deal: {parser.parse(event.message)}")
        await event.message.forward_to(to_chat)



client.loop.run_until_complete(build_id_mappings())
client.run_until_disconnected()
