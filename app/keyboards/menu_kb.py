from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.lexicon.lexicon_ru import (
    LEXICON_MENU_BUTTONS,   
)


# Клавиатура главного меню
def menu_kb() -> ReplyKeyboardMarkup:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text=LEXICON_MENU_BUTTONS['announcements'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['projects'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['rent'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['pictures'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['project'])
    menu_builder.adjust(2)
    return menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)