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

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
buttons = [[KeyboardButton(text="Разработка"), KeyboardButton(text="Администрирование")],
           [KeyboardButton(text="Дизайн"), KeyboardButton(text="Менеджмент")],
           [KeyboardButton(text="Маркетинг"), KeyboardButton(text="Научпоп")]]
kb = ReplyKeyboardMarkup(keyboard=buttons,
                         resize_keyboard=True)


# команда старт
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Привет, {hbold(message.from_user.full_name)}! Из какого раздела ты хочешь получить статьи?",
        reply_markup=kb)


# команда help с описанием работы бота
@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(text=config.HELP_COMMAND)


@dp.message()
async def flow_command(message: Message) -> None:
    # await message.answer(text="WORKED")
    if message.text in config.FLOWS.keys():
        flow = parser.parse_by_flow(config.FLOWS[message.text])
    else:
        await message.answer("Не понял...")
        return
    result_str = "Вот свежайшие статьи, которые могут тебя заинтересовать по теме <b>{}</b>\n\n".format(message.text)
    for article in flow:
        # название статьи
        result_str += "<b>{}</b>\n".format(article.title)
        # автор
        result_str += "<b>Автор:</b> {}\n".format(article.author)
        # URL
        result_str += "<a href='{}'>ссылка на статью</a>\n\n".format(article.url)
    await message.answer(result_str)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.TOKEN_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
