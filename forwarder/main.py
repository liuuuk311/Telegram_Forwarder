from telethon.sync import TelegramClient, events
import requests

api_id = 3052860
api_hash = "c309b7d34c3c15d0f0dac5b503711e9b"

# TelegramClient('prod.session', api_id, api_hash).start()


url = "https://firebasestorage.googleapis.com/v0/b/test1-ba648.appspot.com/o/prod.session?alt=media&token=86f917cc-e2e3-4fd8-9dea-1af759b40174"
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
client.start()
client.send_message('me', 'Rubo le offerte con questo account')


@client.on(events.NewMessage(chats=FROM_CHATS))
async def handler(event):
    to_chat = await client.get_entity(DEAL_GROUP)
    await event.message.forward_to(to_chat)

client.run_until_disconnected()
