from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_about_project_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Добавить/изменить презентацию',
            callback_data='add change presentation',
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Назад в меню ↩️', callback_data='back admin panel from project'
        )
    )
    kb.adjust(1)
    return kb.as_markup()


def cancel_upload_presentation() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text='Отмена', callback_data='cancel upload presentation')
    )
    return kb.as_markup()
