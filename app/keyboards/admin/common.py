from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_panel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Блок Аренда',
            callback_data='admin rent',
        )
    )
    kb.add(InlineKeyboardButton(text='Блок Картины', callback_data='admin picture'))
    kb.add(
        InlineKeyboardButton(text='Блок О Проекте', callback_data='admin about project')
    )
    kb.adjust(1)
    return kb.as_markup()