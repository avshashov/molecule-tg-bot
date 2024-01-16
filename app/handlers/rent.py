from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import CRUDBlockText, CRUDMedia
from app.keyboards.menu_kb import menu_kb
from config import config
from app.constants import PictureStatus, BlockText, MediaType, MediaBlock
from app.fsm.fsm import FSMRent
from app.keyboards.rent_kb import (
    cancel_rent,
    communication_method,
    rent,
    rental_request,
    send,
    send_contact,
)
from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_RENT
from app.text_creator import TextCreator

router = Router()


# Хендлер на кнопку меню 'Аренда'
@router.message(F.text == LEXICON_MENU_BUTTONS['rent'])
async def rent_button(message: Message, session: AsyncSession):
    rent_text = await CRUDBlockText.get_text_by_block(session, block=BlockText.RENT)
    if rent_text:
        await message.answer(text=rent_text, parse_mode=ParseMode.MARKDOWN_V2)
    media = await CRUDMedia.get_media(
        session, media_type_id=MediaType.PHOTO, media_block_id=MediaBlock.RENT
    )
    if media:
        media = [InputMediaPhoto(media=photo.media_id) for photo in media]
        await message.answer_media_group(media=media)
    await message.answer(text='Оставляй заявку прямо здесь 👇', reply_markup=rent())


# Хендлер на кнопку "cancel"
@router.callback_query(F.data == 'cancel_button', ~StateFilter(default_state))
async def cancel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RENT['cancel'], reply_markup=rental_request()
    )
    await state.clear()


# Хендлер на кнопку 'Оставить заявку на аренду помещения' и кнопку 'Исправить'
# Устанавливает состояние ввода телефона
@router.callback_query(F.data == 'repeat_request', StateFilter(FSMRent.send_rent))
@router.callback_query(F.data == 'rental_request')
async def rental_request_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON_RENT['telephone'], reply_markup=send_contact()
    )
    await state.set_state(FSMRent.enter_telephone)


# Хендлер на введенный номер телефона или на присланный контакт,
# переводит в состояние ожидания выбора способа связи
@router.message(StateFilter(FSMRent.enter_telephone))
async def telephone_sent(message: Message, state: FSMContext):
    if (message.text and message.text.isdigit()) or message.contact:
        await message.answer(text='👍', reply_markup=ReplyKeyboardRemove())
        if message.text:
            await state.update_data(enter_telephone=message.text)
        elif message.contact:
            await state.update_data(enter_telephone=message.contact.phone_number)
        await message.answer(
            text=LEXICON_RENT['how_contact'], reply_markup=communication_method()
        )
        await state.set_state(FSMRent.how_contact)
    else:
        await message.answer(
            text=f'{LEXICON_RENT["not_telephone"]}\n\n' f'{LEXICON_RENT["breaking"]}',
            reply_markup=cancel_rent(),
        )


# Хендлер на кнопки выбора способа связи,
# переводит в состояние ожидания ввода даты
@router.callback_query(
    StateFilter(FSMRent.how_contact), F.data.in_(['call', 'telegram', 'whatsapp'])
)
async def how_contact_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.delete()  # Удалить сообщение с кнопками
    await callback.message.answer(
        text=f'Ты выбрал - {LEXICON_RENT[callback.data]}\n\n' f'{LEXICON_RENT["date"]}'
    )
    await state.set_state(FSMRent.date)


# Хендлер будет срабатывать, если во время выбора способа связи
# будет отправлено что-то некорректное
@router.message(StateFilter(FSMRent.how_contact))
async def warning_not_contact(message: Message):
    await message.answer(
        text=f'{LEXICON_RENT["not_contact"]}\n\n' f'{LEXICON_RENT["breaking"]}',
        reply_markup=cancel_rent(),
    )


# Хендлер на введенную дату,
# переводит в состояние ожидания ввода мероприятия
@router.message(StateFilter(FSMRent.date))
async def date_sent(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer(text=LEXICON_RENT['event'])
    await state.set_state(FSMRent.event)


# Хендлер на введенное мероприятие,
# переводит в состояние ожидания ввода количества человек
@router.message(StateFilter(FSMRent.event))
async def event_sent(message: Message, state: FSMContext):
    await state.update_data(event=message.text)
    await message.answer(text=LEXICON_RENT['how_people'])
    await state.set_state(FSMRent.how_people)


# Хендлер на введенное количество человек,
# переводит в состояние завершения формирования заявки
@router.message(StateFilter(FSMRent.how_people))
async def how_people_sent(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text
    if text.isdigit():
        await state.update_data(how_people=message.text)
        data = await state.get_data()
        text = await TextCreator.create_text_rent(
            session, user_id=message.from_user.id, mode=PictureStatus.RENT, **data
        )
        await message.answer(
            text=f'{LEXICON_RENT["finish"]}\n\n' f'{text}',
            reply_markup=send(),
        )
        await state.set_state(FSMRent.send_rent)
        await state.update_data(text=text)
    else:
        await message.answer(
            text=f'{LEXICON_RENT["not_people"]}\n\n' f'{LEXICON_RENT["breaking"]}',
            reply_markup=cancel_rent(),
        )


# Хендлер на кнопку 'Отправить'
@router.callback_query(StateFilter(FSMRent.send_rent), F.data == 'send')
async def send_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer(text=LEXICON_RENT['sending'])
    # Отправка пользователю данных заявки
    await callback.message.answer(text=f'{data["text"]}', reply_markup=menu_kb())
    # Отправка заявки в чат с админами
    await bot.send_message(chat_id=config.tg_bot.admin_group_id, text=f'{data["text"]}')
    await state.clear()
