from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_PICTURES, LEXICON_RENT
from database.database import users_db
from keyboards.keyboards import (
    pictures,
    buy_ready,
    method_contact,
    send_contact,
    send,
)
from config_data.config import config

from aiogram.fsm.context import FSMContext
from fsm.fsm import FSM_PICTURE
from aiogram.fsm.state import default_state


router = Router()


# Хендлер на кнопку меню 'Картины'
@router.message(F.text == LEXICON_MENU_BUTTONS['pictures'])
async def pictures_button(message: Message):
    await message.answer(text=LEXICON_PICTURES['pictures'], reply_markup=pictures())


# Хендлер на кнопку 'Купить готовую'
@router.callback_query(F.data == 'buy_ready')
async def buy_button(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_PICTURES['buy_ready_description'], reply_markup=buy_ready())
    await callback.answer()


# Хендлер на кнопку 'Свяжитесь со мной'
@router.callback_query(F.data == 'contact_me')
async def contact_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_PICTURES['how_contact_2'], reply_markup=method_contact())
    await callback.answer()
    await state.set_state(FSM_PICTURE.how_contact)


# Хендлер на кнопки 'Звонок', 'whatsapp', 'telegram'
@router.callback_query(StateFilter(FSM_PICTURE.how_contact), F.data.in_(['call', 'telegram', 'whatsapp']))
async def how_contact(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.answer(text=LEXICON_PICTURES['number'], reply_markup=send_contact())
    await state.set_state(FSM_PICTURE.enter_telephone)


# Хендлер на кнопку 'email'
@router.callback_query(StateFilter(FSM_PICTURE.how_contact), F.data == 'email')
async def email_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_PICTURES['enter_email'])
    await state.set_state(FSM_PICTURE.enter_email)


# Хендлер на введенный номер телефона или на присланный контакт
@router.message(StateFilter(FSM_PICTURE.enter_telephone))
@router.message(F.contact, StateFilter(FSM_PICTURE.enter_telephone))
async def contact_sent(message: Message, state: FSMContext):
    await message.answer(text='👍', reply_markup=ReplyKeyboardRemove())
    if (message.text and message.text.isdigit()) or message.contact:
        if message.text:
            await state.update_data(enter_telephone=message.text)
        elif message.contact:
            await state.update_data(enter_telephone=message.contact.phone_number)
    else:
        await message.answer(text=f'{LEXICON_RENT["not_telephone"]}\n\n' f'{LEXICON_PICTURES["breaking"]}')

    id = message.from_user.id
    data = await state.get_data()
    await state.clear()

    # Формирование сообщения
    text = f'''Имя: {users_db[id]["name"]}
Телефон: {data["enter_telephone"]}
Способ связи: {data["how_contact"]}\n'''

    await message.answer(
        text=f'Проверь данные -\n\n{text}\nЕсли верно - жми "Отправить", если нет - "Исправить"',
        reply_markup=send(),
    )
    await state.update_data(text=text)
