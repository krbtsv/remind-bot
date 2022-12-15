from logging import StreamHandler, getLogger

import settings
from clients.client_db import SQLiteClient
from clients.telegram_client import TelegramClient

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

BOT_TOKEN = settings.BOT_TOKEN
ADMIN_CHAT_ID = settings.ADMIN_CHAT_ID


class Reminder:
    GET_TASKS = """
        SELECT chat_id FROM users WHERE last_updated_date IS NULL OR last_updated_date < date('now');
        """

    def __init__(self, telegram_client: TelegramClient, database_client: SQLiteClient):
        self.telegram_client = telegram_client
        self.database_client = database_client
        self.setted_up = False

    def setup(self):
        self.database_client.create_conn()
        self.setted_up = True

    def shutdown(self):
        self.database_client.close_conn()

    def notify(self, chat_ids: list):
        for chat_id in chat_ids:
            res = self.telegram_client.post(method='sendMessage',
                                            params={'text': 'Пора отчитаться о проделанной работе!',
                                                    'chat_id': chat_id})
            logger.info(res)

    def execute(self):
        chat_ids = self.database_client.execute_select_command(self.GET_TASKS)
        if chat_ids:
            self.notify(chat_ids=[tuple_from_database[0] for tuple_from_database in chat_ids])

    def __call__(self, *args, **kwargs):
        if not self.setted_up:
            logger.error('Resources in worker has not been set up!')
            return
        self.execute()


if __name__ == '__main__':
    database_client = SQLiteClient('/home/max/PycharmProjects/remind_bot/users.db')
    telegram_client = TelegramClient(token=BOT_TOKEN, base_url='https://api.telegram.org')
    reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
    reminder.setup()
    reminder()
