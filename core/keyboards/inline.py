from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


builder = InlineKeyboardBuilder()


builder.row(
    InlineKeyboardButton(text="ANDIJON", callback_data='andijan'),
    InlineKeyboardButton(text="BUXORO", callback_data='bukhara'),
    InlineKeyboardButton(text="JIZZAX", callback_data='jizzakh'),
    InlineKeyboardButton(text="QASHQADARYO", callback_data='qarshi'),
    InlineKeyboardButton(text="NAVOIY", callback_data='navoi'),
    InlineKeyboardButton(text="NAMANGAN", callback_data='namangan'),
    InlineKeyboardButton(text="SAMARQAND", callback_data='samarkand'),
    InlineKeyboardButton(text="SURXONDARYO", callback_data='termez'),
    InlineKeyboardButton(text="SIRDARYO", callback_data='gulistan'),
    InlineKeyboardButton(text="TOSHKENT", callback_data='tashkent'),
    InlineKeyboardButton(text="FARG'ONA", callback_data='ferghana'),
    InlineKeyboardButton(text="XORAZM", callback_data='urgench'),
    InlineKeyboardButton(text="Qoraqalpog'iston", callback_data='nukus'),
    width=2
)


inline_regions_list_keyboard = builder.as_markup()

answermenu = InlineKeyboardBuilder()

answermenu.row(
    InlineKeyboardButton(text="⬅️ Orqaga", callback_data='prev'),
    InlineKeyboardButton(text="Oldinga ➡️", callback_data='next'),
    width=1
)

inline_answer_menu = answermenu.as_markup()
