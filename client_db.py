import sqlite3


class SQLiteClient:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def execute_command(self, command: str, params: tuple):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("you need to create connection to database!")

    def execute_select_command(self, command: str):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("you need to create connection to database!")


class UserActioner:
    CREATE_USER = """
        INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
        """

    GET_USER = """
        SELECT user_id, username, chat_id FROM users WHERE user_id = %s;
        """

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else []

    def create_user(self, user_id: str, username: str, chat_id: int):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id))


user_actioner = UserActioner(SQLiteClient("users.db"))
user_actioner.setup()
user = user_actioner.get_user("1")
print(user)
user_2 = {"user_id": 3, "username": "test", "chat_id": 11235}
user_actioner.create_user(**user_2)
