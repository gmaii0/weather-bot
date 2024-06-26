from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.keyboards.menu import start_menu

basic_router = Router()


@basic_router.message(CommandStart)
async def get_start(message: Message):
    await message.answer(f"<b>Assalomu alaykum Ob-havo va  havo sifati ko'rsatkichlari (AQI) haqida \
     ma'lumot beruvchi botga hush kelibsiz! </b>", reply_markup=start_menu)
