from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

regions = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="ANDIJON"),
        KeyboardButton(text="BUXORO")
    ],
    [
        KeyboardButton(text="JIZZAX"),
        KeyboardButton(text="QASHQADARYO")
    ],
    [
        KeyboardButton(text="NAVOIY"),
        KeyboardButton(text="NAMANGAN")
    ],
    [
        KeyboardButton(text="SAMARQAND"),
        KeyboardButton(text="SURXONDARYO")
    ],
    [
        KeyboardButton(text="SIRDARYO"),
        KeyboardButton(text="TOSHKENT")
    ],
    [
        KeyboardButton(text="FARG'ONA"),
        KeyboardButton(text="XORAZM")
    ],
],
    resize_keyboard=True, one_time_keyboard=True, width=2
)
