import sqlite3
import psycopg2
from config import config


def update_datetime(column_name, user_id):
    """update datetime of last request in topic for this user"""
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"update public.users set {column_name} = current_timestamp where user_id = '{user_id}'")
            conn.commit()


def get_datetime(user_id, column_name):
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"select {column_name} from public.users where user_id = '{user_id}'")
            return cursor.fetchone()[0]


def user_exists(user_id):
    """check if user exists"""
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"select user_id from public.users where user_id = '{user_id}'")
            return bool(len(cursor.fetchall()))


def create_user(user_id, user_name):
    """create user if it doesn't exist"""
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cursor:
            if not user_exists(user_id):
                cursor.execute(f"insert into public.users (user_id, user_name) values ('{user_id}', '{user_name}')")
                conn.commit()
                return f"Добро пожаловать в бота, {user_name}!"
            else:
                return f"Рады твоему возвращению, {user_name}!"
