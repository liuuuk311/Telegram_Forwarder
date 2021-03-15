
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters

from forwarder import updater, dispatcher

from config import Config

PM_START_TEXT = """
Hey {}, I'm {}!
I'm a bot used to forward messages from one chat to another.

To obtain a list of commands, use /help.
"""

PM_HELP_TEXT = """
Here is a list of usable commands:
 - /start : Starts the bot.
 - /help : Sends you this help message.

just send /id in private chat/group/channel and i will reply it's id.
"""

def start(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]

    if chat.type == "private":
        message.reply_text(PM_START_TEXT.format(user.first_name, dispatcher.bot.first_name), parse_mode=ParseMode.HTML)
    else:
        message.reply_text("I'm up and running!")


def help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not chat.type == "private":
        message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        message.reply_text(PM_HELP_TEXT)


def main():
    start_handler = CommandHandler("start", start, filters=Filters.user(Config.OWNER_ID), run_async=True)
    help_handler = CommandHandler("help", help, filters=Filters.user(Config.OWNER_ID), run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    if Config.WEBHOOK:
        updater.start_webhook(listen=Config.IP_ADDRESS,
                              port=Config.PORT,
                              url_path=Config.API_KEY)

        updater.bot.set_webhook(url=Config.URL + Config.API_KEY)

    else:
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == '__main__':
    main()
