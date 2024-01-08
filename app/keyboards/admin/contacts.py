from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def contacts_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Добавить/изменить контакты',
            callback_data='add edit contacts',
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Назад в меню ↩️', callback_data='back admin panel from contacts'
        )
    )
    kb.adjust(1)
    return kb.as_markup()
