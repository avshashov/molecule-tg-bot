from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_PICTURES, LEXICON_RENT


# Клавиатура кнопки "Картины"
def pictures() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['buy_ready'], callback_data='buy_ready'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['order_painting'], callback_data='order_painting'
        )
    )
    kb.row(
        *[
            InlineKeyboardButton(
                text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'
            ),
            # TODO: включить как будет готов сайт
            # InlineKeyboardButton(
            #     text=LEXICON_PICTURES['online_gallery'], callback_data='online_gallery'
            # ),
        ],
        width=1
    )
    return kb.as_markup()


# Клавиатура кнопки "Купить готовую"
def buy_ready() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['catalog_paintings'],
            url='https://disk.yandex.ru/d/1MSKch2JtaetfA',
        )
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['contact_me'], callback_data='contact_me'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['back'], callback_data='back_pictures'
        )
    )
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора способа связи
def method_contact(picture_is_ready: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['call'], callback_data='call'))
    kb.add(
        InlineKeyboardButton(text=LEXICON_RENT['telegram'], callback_data='telegram')
    )
    kb.add(
        InlineKeyboardButton(text=LEXICON_RENT['whatsapp'], callback_data='whatsapp')
    )
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['email'], callback_data='email'))
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['cancel_button'],
            callback_data=f'cancel_button_pictures {picture_is_ready}',
        )
    )
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура - кнопка 'Отправить' и кнопка 'Исправить'
def send_correct() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text=LEXICON_RENT['send'], callback_data='send_contact')
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_RENT['repeat_request'], callback_data='correct'
        )
    )
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура - кнопка 'Отменить'
def cancel_picture() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_PICTURES['cancel_button'],
            callback_data='cancel_button_pictures',
        )
    )
    return kb.as_markup()


# Клавиатура - кнопка 'Пропустить вопрос'
def skip() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=LEXICON_PICTURES['skip'])
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
