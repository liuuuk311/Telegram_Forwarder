import asyncio
import logging
import os

from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events

from forwarder.settings import CHANNELS_MAPPING, FORMATTERS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("Forwarder Bot")

api_id = os.getenv("APP_ID")
api_hash = os.getenv("api_hash")

# Uncomment when we need a new session key
# generate_new_session_key(api_id, api_hash)

session_key = os.getenv("SESSION_KEY")


client = TelegramClient(StringSession(session_key), api_id, api_hash)
client.start()
MAPPINGS = {}


async def build_id_mappings():
    for channel, settings in CHANNELS_MAPPING.items():
        entity = await client.get_entity(channel)
        peer_id = await client.get_peer_id(entity)
        settings.parser.client = client
        MAPPINGS[peer_id] = settings

    logger.info(f"Mappings: {MAPPINGS}")


@client.on(events.NewMessage)
async def generic_handler(event: events.NewMessage.Event):
    sender = await event.get_sender()
    logger.info(f"New event from: {sender.username}")
    channel_settings = MAPPINGS.get(event.chat_id)

    if not channel_settings:
        return

    logger.info("Channel settings available!")
    parsed = await channel_settings.parser.parse(event)
    if not parsed.is_valid:
        logger.warning(
            f"Parsed messaged from {sender.username} and is NOT VALID: {parsed}"
        )
        logger.warning(f"REASON: {parsed.reason_not_valid}")
        return

    formatter = FORMATTERS.get(channel_settings.destination_channel)(parsed_deal=parsed)
    await client.send_message(
        entity=channel_settings.destination_channel,
        message=formatter.get_message_text(),
        link_preview=False,
        file=parsed.image,
    )
    logger.info("YEAH! Forward successful!")
    await asyncio.sleep(5)


@client.on(events.NewMessage(from_users=["@iamlucafpv"]))
async def test(event: events.NewMessage.Event):
    sender = await event.get_sender()
    logger.info(f"New event from: {sender.username}")
    entity = await client.get_entity("@fpvmattia")
    peer_id = await client.get_peer_id(entity)
    channel_settings = MAPPINGS.get(peer_id)

    if not channel_settings:
        return

    logger.info("Channel settings available!")
    parsed = await channel_settings.parser.parse(event)
    if not parsed.is_valid:
        logger.warning(
            f"Parsed messaged from {sender.username} and is NOT VALID: {parsed}"
        )
        logger.warning(f"REASON: {parsed.reason_not_valid}")
        return

    formatter = FORMATTERS.get(channel_settings.destination_channel)(
        parsed_deal=parsed
    )
    await client.send_message(
        entity=channel_settings.destination_channel,
        message=formatter.get_message_text(),
        link_preview=False,
        file=parsed.image,
    )
    logger.info("YEAH! Forward successful!")
    await asyncio.sleep(5)


client.loop.run_until_complete(build_id_mappings())
client.run_until_disconnected()
