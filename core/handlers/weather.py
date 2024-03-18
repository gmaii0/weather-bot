from aiogram.types import Message, message
from aiogram import Router, Bot, F
from core.settings import settings

find_router = Router

async def get_weather(city, OPENWEATHER_API_TOKEN):
    pass

@find_router.message(F.text == "ANDIJON")
async def get_and():
    await message.reply("ID kiriting")