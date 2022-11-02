import sqlite3

CREATE_USER = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

GET_USER = """
    SELECT user_id, username, chat_id FROM users WHERE user_id = %s;
    """


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


sqlite_client = SQLiteClient("users.db")
sqlite_client.create_conn()
sqlite_client.execute_command(CREATE_USER, (3, "max3", 1233))
print(sqlite_client.execute_select_command(GET_USER % (1,)))
