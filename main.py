from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import State, StatesGroup 
from environs import Env

import logging
import asyncio

env = Env()
env.read_env()

dp = Dispatcher()
TOKEN = env.str("TOKEN")


@dp.message(CommandStart())
async def start_commit(message: Message):
    

    lang = ReplyKeyboardMarkup(
        keyboard= [
            [KeyboardButton(text="🇺🇿 uz"), KeyboardButton(text="🇺🇸 en")],
            [KeyboardButton(text="🇷🇺 ru"), KeyboardButton(text="🇸🇦 ar")]
				],resize_keyboard=True
		)

    await message.answer(text, reply_markup=lang)


@dp.message(F.text=="🇺🇿 uz")
async def lan_uz(message:Message): 
    name_kb =ReplyKeyboardMarkup(
        keyboard= [
            [KeyboardButton(text="Register:")]
				],resize_keyboard=True
		)
    
    await message.answer(f"🔑 Kirish uchun ro‘yxatdan o‘ting.",reply_markup=name_kb)
		



async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
