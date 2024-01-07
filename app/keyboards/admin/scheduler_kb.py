from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database import models


def picture_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Добавить картину', callback_data='add picture'))
    kb.add(
        InlineKeyboardButton(
            text='Редактирование картин', callback_data='edit pictures'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Назад в меню ↩️', callback_data='back admin panel from pictures'
        )
    )
    kb.adjust(1)
    return kb.as_markup()


def back_pictures_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back pictures menu'))
    return kb.as_markup()


def list_of_current_pictures_kb(
    pictures: list[models.Picture],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if pictures:
        for picture in pictures:
            kb.add(
                InlineKeyboardButton(text=picture.title, callback_data=str(picture.id))
            )
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back pictures menu'))
    kb.adjust(1)
    return kb.as_markup()


def open_picture_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Изменить заголовок ✏️', callback_data='change picture title'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Изменить описание ✏️', callback_data='change picture description'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Удалить картину ❌', callback_data='delete picture menu'
        )
    )
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back to list pictures'))
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_picture_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Подтвердить удаление ❌', callback_data='confirm delete picture'
        )
    )
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='cancel delete picture'))
    kb.adjust(1)
    return kb.as_markup()
