from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from core.keyboards.menu import regions

start_router = Router()
@start_router.message(CommandStart)
async def get_start(message: Message, bot: Bot):
    await message.answer(f"<b>Ro'yxatda berilgan viloyatni tanlang</b>", reply_markup=regions)

