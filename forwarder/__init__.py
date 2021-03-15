import logging
import os

import telegram.ext as tg

# enable logging
from forwarder.config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

updater = tg.Updater(Config.API_KEY, workers=Config.WORKERS)
dispatcher = updater.dispatcher