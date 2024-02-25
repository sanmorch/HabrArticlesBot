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
        text=parser.BotDB.create_user(message.from_user.id, message.from_user.first_name),
        reply_markup=kb)


# help command
@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(text=config.HELP_COMMAND)


@dp.message()
async def flow_command(message: Message) -> None:
    # await message.answer(text="WORKED")

    if message.text in config.FLOWS.keys():
        flow = parser.parse_by_flow(config.FLOWS[message.text])
    else:
        await message.answer("Такого я еще не знаю")
        return
    result_str = "Вот свежайшие статьи, которые могут тебя заинтересовать по теме <b>{}</b>\n\n".format(message.text)
    for article in flow:
        # название статьи
        result_str += f"<b>{article.title}</b>\n<b>Автор:</b> {article.author}\n<a href='{article.url}'>ссылка на статью</a>\n\n"
    await message.answer(parser.BotDB.update_datetime(config.FLOWS[message.text], message.from_user.id))
    await message.answer(result_str)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.TOKEN_API, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
