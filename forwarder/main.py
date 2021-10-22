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
client.send_message('me', 'Rubo le offerte con questo account')

allowed_to_send_amazon_tracking_command = ""


@client.on(events.NewMessage(chats=FROM_CHATS))
async def handler(event):
    to_chat = await client.get_entity(DEAL_GROUP)
    await event.message.forward_to(to_chat)


@client.on(events.NewMessage(pattern=r"https:\/\/(www.)?(amazon\.it|amzn\.to)\/(\w*-?\/?\??=?&?)*"))
async def amazon_tracker_forward_handler(event):
    test = await client.get_entity('t.me/traccia_prezzo_bot')
    print(event.chat)
    await event.message.forward_to(test)


client.run_until_disconnected()
