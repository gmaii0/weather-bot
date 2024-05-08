from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.keyboards.inline import inline_regions_list_keyboard


basic_router = Router()
@basic_router.message(CommandStart)
async def get_start(message: Message):
    await message.answer(f"<b>Ro'yxatda berilgan viloyatni tanlang</b>", reply_markup=inline_regions_list_keyboard)

