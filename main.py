import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

API_TOKEN = "8249854204:AAHBtu8M22evD10YxzPdONyecesP0atlF74"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_data = {}

lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="UZ"), KeyboardButton(text="RU"), KeyboardButton(text="EN")]
    ],
    resize_keyboard=True
)

def reg_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text={"UZ":"Ro'yxatdan o'tish","RU":"Регистрация","EN":"Register"}[lang])]],
        resize_keyboard=True
    )

def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]],
        resize_keyboard=True
    )

def location_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Joylashuv yuborish", request_location=True)]],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Tilni tanlang:", reply_markup=lang_kb)

@dp.message(F.text.in_(["UZ", "RU", "EN"]))
async def lang_handler(message: Message):
    user_data[message.from_user.id] = {"lang": message.text}
    await message.answer("Til o'zgardi ✅", reply_markup=reg_kb(message.text))

@dp.message(F.text.in_(["Ro'yxatdan o'tish", "Регистрация", "Register"]))
async def register_handler(message: Message):
    user_data[message.from_user.id]["step"] = "name"
    await message.answer("Ismingizni kiriting:")

@dp.message(lambda m: user_data.get(m.from_user.id, {}).get("step") == "name")
async def name_handler(message: Message):
    uid = message.from_user.id
    user_data[uid]["name"] = message.text
    user_data[uid]["step"] = "phone"
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_kb())

@dp.message(F.contact)
async def phone_handler(message: Message):
    uid = message.from_user.id
    user_data[uid]["phone"] = message.contact.phone_number
    user_data[uid]["step"] = "location"
    await message.answer("Joylashuvingizni yuboring:", reply_markup=location_kb())

@dp.message(F.location)
async def location_handler(message: Message):
    uid = message.from_user.id
    user_data[uid]["location"] = (message.location.latitude, message.location.longitude)
    user_data[uid]["step"] = "done"
    await message.answer(
        f"Ro'yxatdan o'tildi ✅\n"
        f"Ism: {user_data[uid]['name']}\n"
        f"Telefon: {user_data[uid]['phone']}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
