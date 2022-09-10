import telebot
from telebot.types import Message
import json

import settings
import requests
from datetime import datetime

bot_client = telebot.TeleBot(token=settings.BOT_TOKEN)


@bot_client.message_handler(commands=["start"])
def start(message: Message):
    with open("users.json", "r") as file_obj:
        data_from_json = json.load(file_obj)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}

    with open("users.json", "w") as file_obj:
        json.dump(data_from_json, file_obj, indent=4, ensure_ascii=False)

    bot_client.reply_to(message=message, text=str(f"Вы зарегистрированы: {username}.\nВаш user_id: {user_id}"))


def handle_about_day(message: Message):
    bot_client.reply_to(message, 'Отлично! Ты хорошо потрудился!')


@bot_client.message_handler(commands=["say_about_day"])
def say_about_day(message: Message):
    bot_client.reply_to(message, text='Привет! Чем сегодня занимался?')
    bot_client.register_next_step_handler(message, callback=handle_about_day)


while True:
    try:
        bot_client.polling()
    except Exception as err:
        requests.post(settings.ERROR_MESSAGE + f'&text={datetime.now()} ::: {err.__class__} ::: {err}')
