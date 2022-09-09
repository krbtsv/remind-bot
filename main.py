import telebot
from telebot.types import Message
import json

import settings

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


bot_client.polling()
