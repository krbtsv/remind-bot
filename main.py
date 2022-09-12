import telebot
from telebot.types import Message
import json

import settings
import requests
from datetime import datetime

from telegram_client import TelegramClient


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client


telegram_client = TelegramClient(token=settings.BOT_TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=settings.BOT_TOKEN, telegram_client=telegram_client)


@bot.message_handler(commands=["start"])
def start(message: Message):
    with open("users.json", "r") as file_obj:
        data_from_json = json.load(file_obj)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}

    with open("users.json", "w") as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)

    bot.reply_to(message=message, text=str(f"Вы зарегистрированы: {username}.\nВаш user_id: {user_id}"))


def handle_about_day(message: Message):
    bot.reply_to(message, 'Отлично! Ты хорошо потрудился!')


@bot.message_handler(commands=["say_about_day"])
def say_about_day(message: Message):
    bot.reply_to(message, text='Привет! Чем сегодня занимался?')
    bot.register_next_step_handler(message, callback=handle_about_day)


def create_err_message(err: Exception) -> str:
    return f"{datetime.now()} ::: {err.__class__} ::: {err}"


while True:
    try:
        bot.polling()
    except Exception as err:
        bot.telegram_client.post(method="sendMessage", params={"chat_id": settings.ADMIN_CHAT_ID,
                                                               "text": create_err_message(err)})
