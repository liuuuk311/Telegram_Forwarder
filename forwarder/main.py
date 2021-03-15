from telethon.sync import TelegramClient, events
import requests

api_id = 3877185
api_hash = "a71f3afb87f37c887e2373ee401ffc66"
TelegramClient('login.session', api_id, api_hash).start()


# api_id = 2840733
# api_hash = "51c7559051fc35ca378e6ea4ed6cccc9"


url = "https://firebasestorage.googleapis.com/v0/b/test1-ba648.appspot.com/o/login.session?alt=media&token=978195ad-6c9f-4a9a-92c0-f27d7ac38f0f"
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

with TelegramClient('login.session', api_id, api_hash) as client:

   from_entity = [client.get_entity(chat_id) for chat_id in FROM_CHATS]
   to_chat = client.get_entity(-405845918)

   @client.on(events.NewMessage(chats=from_entity))
   async def handler(event):
      await event.message.forward_to(to_chat)

   client.run_until_disconnected()
