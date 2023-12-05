from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_MENU_BUTTONS, LEXICON_ABOUT_PROJECT

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
def yes_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RU['of_course'], callback_data='of_course'))
    kb.add(InlineKeyboardButton(text=LEXICON_RU['another name'], callback_data='another name'))
    kb.adjust(2)
    return kb.as_markup()

# Клавиатура подтверждения имени
def yes_no_name_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RU['confirm'], callback_data='confirm'))
    kb.add(InlineKeyboardButton(text=LEXICON_RU['not'], callback_data='not'))
    kb.adjust(2)
    return kb.as_markup()

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

# Клавиатура кнопки "О проекте"
def about_project() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_ABOUT_PROJECT['go_website'], url='https://t.me/Molecule_nebula_bot'))
    kb.add(InlineKeyboardButton(text=LEXICON_ABOUT_PROJECT['download_presentation'], callback_data='download_presentation'))
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
    kb.adjust(1)
    return kb.as_markup()
