from aiogram import Bot
from aiogram.types import Message
from core.keyboards.menu import regions

async def get_start(message: Message, bot: Bot):
    await message.answer(f'<tg-spoiler>Hello {message.from_user}</tg-spoiler>', reply_markup=regions)

