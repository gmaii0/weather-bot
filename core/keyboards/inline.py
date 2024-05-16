from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_keyboard(buttons, width=2):
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(width)
    return builder.as_markup()

region_buttons = [
    ("ANDIJON", 'loc_40.77_72.34'),
    ("BUXORO", 'loc_39.77_64.43'),
    ("JIZZAX", 'loc_40.12_67.83'),
    ("QASHQADARYO", 'loc_38.85_65.78'),
    ("NAVOIY", 'loc_40.09_65.38'),
    ("NAMANGAN", 'loc_41.00_71.67'),
    ("SAMARQAND", 'loc_39.66_66.96'),
    ("SURXONDARYO", 'loc_37.23_67.28'),
    ("SIRDARYO", 'loc_40.86_68.78'),
    ("TOSHKENT", 'loc_41.32_69.27'),
    ("FARG'ONA", "loc_40.39_71.78"),
    ("XORAZM", 'loc_41.53_60.63'),
    ("Qoraqalpog'iston", 'loc_42.47_59.62')
]

navigation_buttons = [
    ("🍃 Havo sifati indeksi", 'index'),
    ("⬅️ Orqaga", 'prev')
]

inline_regions_list_keyboard = create_inline_keyboard(region_buttons)

inline_answer_menu = create_inline_keyboard(navigation_buttons, width=1)

inline_back_button = create_inline_keyboard([("⬅️ Orqaga", 'prev')], width=1)