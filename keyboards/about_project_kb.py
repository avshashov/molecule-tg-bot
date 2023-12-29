from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import (
    LEXICON_MENU_BUTTONS,
    LEXICON_ABOUT_PROJECT,
)

# Клавиатура кнопки "О проекте"
def about_project() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_ABOUT_PROJECT['go_website'], url='https://t.me/Molecule_nebula_bot'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_ABOUT_PROJECT['download_presentation'], callback_data='download_presentation'
        )
    )
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
    kb.adjust(1)
    return kb.as_markup()