from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_PICTURES
from database.database import users_db
from keyboards.keyboards import (
    pictures,
    buy_ready,
    how_contact,
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
    await callback.message.edit_text(text=LEXICON_PICTURES['how_contact_2'], reply_markup=how_contact())
    await callback.answer()
    await state.set_state(FSM_PICTURE.how_contact)


# Хендлер на кнопки 'Звонок', 'whatsapp', 'telegram'
@router.callback_query(StateFilter(FSM_PICTURE.how_contact), F.data.in_(['call', 'telegram', 'whatsapp']))
async def how_contact(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_PICTURES['number'])
    await state.set_state(FSM_PICTURE.enter_telephone)


# Хендлер на кнопку 'email'
