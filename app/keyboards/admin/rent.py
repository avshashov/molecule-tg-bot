from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import models


def rent_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Просмотр блока', callback_data='view rent block'))
    kb.add(
        InlineKeyboardButton(
            text='Изменить текст аренды', callback_data='change rent text'
        )
    )
    kb.add(
        InlineKeyboardButton(text='Редактировать фото', callback_data='edit rent photo')
    )
    kb.add(
        InlineKeyboardButton(text='Назад в меню ↩️', callback_data='back admin panel')
    )
    kb.adjust(1)
    return kb.as_markup()


def edit_rent_photo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Добавить новое фото', callback_data='add new rent photo'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text='Редактировать текущие фото', callback_data='edit current rent photo'
        )
    )
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back rent menu'))
    kb.adjust(1)
    return kb.as_markup()


def cancel_send_rent_photo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='cancel send rent photo'))
    return kb.as_markup()


def list_of_current_rent_photo_kb(
    list_photo: list[models.Media],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if list_photo:
        for photo in list_photo:
            kb.add(InlineKeyboardButton(text=photo.title, callback_data=str(photo.id)))
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back edit rent photo'))
    kb.adjust(1)
    return kb.as_markup()


def open_rent_photo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Изменить заголовок ✏️', callback_data='change rent photo title'
        )
    )
    kb.add(
        InlineKeyboardButton(text='Удалить фото ❌', callback_data='delete rent photo')
    )
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back list rent photo'))
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_rent_photo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Подтвердить удаление ❌', callback_data='confirm delete rent photo'
        )
    )
    kb.add(
        InlineKeyboardButton(text='Отмена', callback_data='cancel delete rent photo')
    )
    kb.adjust(1)
    return kb.as_markup()


def cancel_change_rent_photo_title() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text='Отмена', callback_data='cancel change rent title')
    )
    return kb.as_markup()


def cancel_change_rent_text() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Отмена', callback_data='back rent menu'))
    return kb.as_markup()


def back_rent_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back rent menu'))
    return kb.as_markup()
