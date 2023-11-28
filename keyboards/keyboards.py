from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
yes = KeyboardButton(text=LEXICON_RU['of_course'])
no = KeyboardButton(text=LEXICON_RU['another name'])

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[[yes, no]],
    resize_keyboard=True,
    one_time_keyboard=True)

# Клавиатура главного меню
events_button = KeyboardButton(text=LEXICON_RU['events'])
rent_button = KeyboardButton(text=LEXICON_RU['rent'])
pictures_button = KeyboardButton(text=LEXICON_RU['pictures'])
project_button = KeyboardButton(text=LEXICON_RU['project'])

menu_builder = ReplyKeyboardBuilder()

menu_builder.row(events_button, rent_button, pictures_button, project_button, width=1)

menu_kb: ReplyKeyboardMarkup = menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)