import sqlite3
import psycopg2
from config import config


class BotDB:

    def __init__(self):
        """init connection"""
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """check if user exists"""
        self.cursor.execute(f"select user_id from public.users where user_id = '{user_id}'")
        return bool(len(self.cursor.fetchall()))

    def create_user(self, user_id, user_name):
        """create user if it doesn't exist"""
        if not self.user_exists(user_id):
            self.cursor.execute(f"insert into public.users (user_id, user_name) values ('{user_id}', '{user_name}')")
            self.conn.commit()
            return f"Добро пожаловать в бота, {user_name}!"
        else:
            return f"Рады твоему возвращению, {user_name}!"

    def update_datetime(self, column_name, user_id):
        """update datetime of last request in topic for this user"""
        self.cursor.execute(f"update public.users set {column_name} = current_timestamp where user_id = '{user_id}'")
        self.conn.commit()
        return f"update public.users set {column_name} = current_timestamp where user_id = '{user_id}'"


    def close(self):
        self.conn.close()
