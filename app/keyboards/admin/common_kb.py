from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def admin_panel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Блок Аренда',
            callback_data='admin rent',
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Блок Картины (Рассылка)', callback_data='admin pictures'
        )
    )
    kb.add(
        InlineKeyboardButton(text='Блок О Проекте', callback_data='admin about project')
    )
    kb.add(
        InlineKeyboardButton(
            text='Команда Контакты', callback_data='admin contacts command'
        )
    )
    kb.adjust(1)
    return kb.as_markup()


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Отмена')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
