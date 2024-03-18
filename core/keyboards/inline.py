from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


builder = InlineKeyboardBuilder()


builder.row(
    InlineKeyboardButton(text="ANDIJON", callback_data='akt_confirm'),
    InlineKeyboardButton(text="BUXORO", callback_data='duk_confirm'),
    InlineKeyboardButton(text="JIZZAX", callback_data='duk_leader_confirm'),
    InlineKeyboardButton(text="QASHQADARYO", callback_data='installed'),
    InlineKeyboardButton(text="NAVOIY", callback_data='rejected'),
    InlineKeyboardButton(text="NAMANGAN", callback_data='errors'),
    width=1
)

inline_regions_list_keyboard = builder.as_markup()