from aiogram import Bot, Dispatcher
import asyncio
import betterlogging as bl
import logging
from aiogram.enums import ParseMode
from core.handlers.basic import get_start
from core.settings import settings
import requests

def get_weather(city, openweather_api_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.bots.openweather_api_token}"
        )
        data = r.json()
        print(data)
    except Exception as ex:
        print(ex)
        print("shaxar nomini togri kiriting")

async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='bot started')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='bot stopped')


async def start():
    bl.basic_colorized_config(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(start())
