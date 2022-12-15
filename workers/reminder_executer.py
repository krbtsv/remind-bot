import datetime
import time
from logging import StreamHandler, getLogger

import settings
from clients.client_db import SQLiteClient
from clients.telegram_client import TelegramClient
from workers.reminder import Reminder

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
BOT_TOKEN = settings.BOT_TOKEN
FROM_TIME = settings.FROM_TIME
TO_TIME = settings.TO_TIME
REMINDER_PERIOD = settings.REMINDER_PERIOD
SLEEP_CHECK_PERIOD = int(settings.REMINDER_PERIOD)

database_client = SQLiteClient("/home/max/PycharmProjects/remind_bot/users.db")
telegram_client = TelegramClient(token=BOT_TOKEN,
                                 base_url="https://api.telegram.org")
reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
reminder.setup()

start_time = datetime.datetime.strptime(FROM_TIME, '%H:%M').time()
end_time = datetime.datetime.strptime(TO_TIME, '%H:%M').time()
while True:
    now_time = datetime.datetime.now().time()
    if start_time <= now_time <= end_time:
        reminder()
        time.sleep(REMINDER_PERIOD)
    else:
        time.sleep(SLEEP_CHECK_PERIOD)
