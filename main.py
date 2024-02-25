import asyncio
import logging
import sys
from os import getenv

import aiogram.types.bot_command
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

import config
import parser
import sql_moves

from datetime import datetime

# bot
dp = Dispatcher()

# keyboard with topics
buttons = [[KeyboardButton(text="Разработка"), KeyboardButton(text="Администрирование")],
           [KeyboardButton(text="Дизайн"), KeyboardButton(text="Менеджмент")],
           [KeyboardButton(text="Маркетинг"), KeyboardButton(text="Научпоп")]]
kb = ReplyKeyboardMarkup(keyboard=buttons,
                         resize_keyboard=True)


# start command
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=sql_moves.create_user(message.from_user.id, message.from_user.first_name),
        reply_markup=kb)


# help command
@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(text=config.HELP_COMMAND)


@dp.message()
async def flow_command(message: Message) -> None:
    if message.text in config.FLOWS.keys():
        flow = parser.parse_by_flow(config.FLOWS[message.text])
    else:
        return

    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    last_update = sql_moves.get_datetime(message.from_user.id, config.FLOWS[message.text])
    last_update = datetime.fromisoformat(str(last_update))
    result_str = ""
    for article in flow:
        article_datetime = datetime.strptime(article.time_added,datetime_format)
        if article_datetime >= last_update:
            result_str += f"<b>{article.title}</b>\n" \
                      f"<b>Автор:</b> {article.author}\n" \
                      f"<a href='{article.url}'>ссылка на статью</a>\n\n"
    if len(result_str) == 0:
        result_str = "Поражаюсь твоей любознательности! Ты ищешь статьи быстрее, чем их успевают писать! Пока новых " \
                     "статей по этой теме не появилось :( "
    else:
        result_str = "Вот свежайшие статьи, которые могут тебя заинтересовать по теме <b>{}</b>\n\n".format(message.text) \
                 + result_str
    sql_moves.update_datetime(config.FLOWS[message.text], message.from_user.id)
    await message.answer(result_str)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.TOKEN_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
