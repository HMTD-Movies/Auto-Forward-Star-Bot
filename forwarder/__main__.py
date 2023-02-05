import importlib

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters

from forwarder import (API_KEY, CERT_PATH, IP_ADDRESS, LOGGER, OWNER_ID, PORT,
                       URL, WEBHOOK, dispatcher, updater)
from forwarder.modules import ALL_MODULES

START = """
<b>Hi 👋🏻 {},

I'm {} to Maintain Your Channels. I am very useful for the Channel Admin who have many Channels.

See /help for more Details.

Maintained By :- Karthik</b>
"""

HELP = """
<b>Hi 👋🏻 {},

Here is a list of usable Commands :-
♦️ /start :- Check if 😊 I'm Alive
♦️ /help :- This Bot's Features 
♦️ /about :- to Know About Me 😁
♦️ /id :- Get Your 🆔

just Send /id in Private Chat/Group/Channel and i will Reply it's ID.</b>
"""

ABOUT = """
<b>🤖 My Name : Star Auto Forward Bot

🧑🏻‍💻 Developer : Karthik

📝 Language : Pyrogram

📚 Framework : Python3

📡 Hosted on : VPS

📢 Updates Channel : @Star_Moviess_Tamil</b>
"""

for module in ALL_MODULES:
    importlib.import_module("forwarder.modules." + module)


def start(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if chat.type == "private":
        message.reply_text(
            START.format(user.first_name, dispatcher.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        message.reply_text("I'm up and running!")

def about(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if chat.type == "private":
        message.reply_text(
            ABOUT.format(user.first_name, dispatcher.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        message.reply_text("About Me")

def help(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if chat.type == "private":
        message.reply_text(
            HELP.format(user.first_name, dispatcher.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        message.reply_text("Contact me via PM to get a list of usable commands.")

def main():
    start_handler = CommandHandler(
        "start", start, filters=Filters.user(OWNER_ID), run_async=True
    )
    help_handler = CommandHandler(
        "help", help, filters=Filters.user(OWNER_ID), run_async=True
    )
    about_handler = CommandHandler(
        "about", about, filters=Filters.user(OWNER_ID), run_async=True
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_handler)

    if WEBHOOK and URL:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen=IP_ADDRESS, port=PORT, url_path=API_KEY)

        if CERT_PATH:
            updater.bot.set_webhook(
                url=URL + API_KEY, certificate=open(CERT_PATH, "rb")
            )
        else:
            updater.bot.set_webhook(url=URL + API_KEY)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
