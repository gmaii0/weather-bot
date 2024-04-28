from aiogram import Bot, Router, F
from aiogram.types import Message
from core.keyboards.inline import inline_regions_list_keyboard

check_regions_router = Router()

regions_list = [
    "ANDIJON", "BUXORO", "JIZZAX",
    "QASHQADARYO", "NAVOIY", "NAMANGAN",
    "SAMARQAND", "SURXONDARYO", "SIRDARYO", "TOSHKENT",
    "FARG'ONA", "XORAZM"
]


@check_regions_router.message(F.text == "ANDIJON")
async def check_regions(message: Message):
    await message.answer(f"test", reply_markup=inline_regions_list_keyboard)
