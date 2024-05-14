from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_keyboard(buttons, width=2):
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(width)
    return builder.as_markup()

region_buttons = [
    ("ANDIJON", 'andijan'),
    ("BUXORO", 'bukhara'),
    ("JIZZAX", 'jizzakh'),
    ("QASHQADARYO", 'qarshi'),
    ("NAVOIY", 'navoi'),
    ("NAMANGAN", 'namangan'),
    ("SAMARQAND", 'samarkand'),
    ("SURXONDARYO", 'termez'),
    ("SIRDARYO", 'Sirdaryo'),
    ("TOSHKENT", 'Toshkent'),
    ("FARG'ONA", "Farg'ona"),
    ("XORAZM", 'urgench'),
    ("Qoraqalpog'iston", 'nukus')
]

navigation_buttons = [
    ("⬅️ Orqaga", 'prev')
]

inline_regions_list_keyboard = create_inline_keyboard(region_buttons)
inline_answer_menu = create_inline_keyboard(navigation_buttons, width=1)
