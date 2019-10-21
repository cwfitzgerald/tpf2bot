import sqlite3
import datetime
import shutil
import time
import typing
import os


def open_database(path, init):
    if not os.path.exists(path):
        if not os.path.exists(init):
            print(f"Init database not found at {init}, aborting")
            exit(1)

        shutil.copy(init, path)

    connection = sqlite3.connect(path)

    return Database(connection)


class Database:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    @staticmethod
    def __init_user(cursor: sqlite3.Cursor, user: int):
        cursor.execute("INSERT OR IGNORE INTO users(id) VALUES (?)", (user,))

    def init_users(self, users: typing.List[int]):
        with self.connection:
            cursor = self.connection.cursor()
            for u in users:
                print(u)
                self.__init_user(cursor, u)

    def user_message(self, user: int, channel: int):
        t = datetime.date.fromtimestamp(time.gmtime())

        date = t.strftime("%Y-%m-%d")

        print(f"Message sent {date} from {user} on {channel}")

        with self.connection:
            cursor = self.connection.execute("SELECT count FROM message_count WHERE id=? AND date=? AND channel=?", (user, date, channel))
            count = cursor.fetchone()

            if count is None:
                print(f"Found zero messages")
                cursor.execute("INSERT INTO message_count(id, date, channel, count) VALUES (?, ?, ?, 1)", (user, date, channel))
            else:
                print(f"Found {count} messages")
                cursor.execute("UPDATE message_count SET count = count + 1 WHERE id=? AND date=? AND channel=?", (user, date, channel))

            cursor.execute("UPDATE users SET messages = messages + 1 WHERE id=?",
                           (user,))

    def get_top_on_channel(self, channel: int, date_start: datetime.date, date_end: datetime.date, count: int):
        date_start_str = date_start.strftime("%Y-%m-%d")
        date_end_str = date_end.strftime("%Y-%m-%d")

        with self.connection:
            