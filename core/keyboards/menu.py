from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Hududni tanlash')
        ],
        [
            KeyboardButton(text='📍 Lokatiya orqali', request_location=True)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)