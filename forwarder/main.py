# api_id = 3877185
# api_hash = "a71f3afb87f37c887e2373ee401ffc66"
import requests

api_id = 2840733
api_hash = "51c7559051fc35ca378e6ea4ed6cccc9"

from telethon.sync import TelegramClient, events

url = "https://firebasestorage.googleapis.com/v0/b/test1-ba648.appspot.com/o/login.session?alt=media&token=978195ad-6c9f-4a9a-92c0-f27d7ac38f0f"
r = requests.get(url, allow_redirects=True)
open('login.session', 'wb').write(r.content)

string = ""

with TelegramClient('login.session', api_id, api_hash) as client:

   @client.on(events.NewMessage(incoming=True))
   async def handler(event):
      username = await client.get_entity(-405845918)
      await event.message.forward_to(username)

   client.run_until_disconnected()
