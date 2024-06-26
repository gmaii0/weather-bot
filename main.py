from aiogram import Bot, Dispatcher
import asyncio
import betterlogging as bl
import logging
from core.handlers.basic import basic_router
from core.handlers.location import loc_router
from core.handlers.weather import weather_router
from core.settings import settings
from core.utils.commands import set_commands
from aiogram.enums import ParseMode


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='bot started')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='bot stopped')
    await bot.session.close()


async def start():
    bl.basic_colorized_config(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_router(weather_router)
    dp.include_router(loc_router)
    dp.include_router(basic_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(start())
