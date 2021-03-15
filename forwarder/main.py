from telethon.sync import TelegramClient, events
import requests
import asyncio

api_id = 3877185
api_hash = "a71f3afb87f37c887e2373ee401ffc66"

url = "https://firebasestorage.googleapis.com/v0/b/test1-ba648.appspot.com/o/login.session?alt=media&token=77467350-16b9-4a5d-8321-559397f2e6eb"
r = requests.get(url, allow_redirects=True)
open('login.session', 'wb').write(r.content)

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


client = TelegramClient('login.session', api_id, api_hash)


@client.on(events.NewMessage(chats=FROM_CHATS))
async def handler(event):
    to_chat = await client.get_entity(DEV_GROUP)
    await event.message.forward_to(to_chat)

client.start()
client.run_until_disconnected()
