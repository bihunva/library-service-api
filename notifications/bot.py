import os

import telebot
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(message) -> None:
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

    bot.send_message(chat_id, message)
