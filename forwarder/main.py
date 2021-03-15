# api_id = "3877185"
# api_hash = "a71f3afb87f37c887e2373ee401ffc66"

api_id = 2840733
api_hash = "51c7559051fc35ca378e6ea4ed6cccc9"

from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

string = ""

with TelegramClient(StringSession(string), api_id, api_hash) as client:

   @client.on(events.NewMessage(incoming=True))
   async def handler(event):
      username = await client.get_entity(-405845918)
      await event.message.forward_to(username)

   client.run_until_disconnected()
