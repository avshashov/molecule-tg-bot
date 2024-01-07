from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from config import config
from app.constants import PictureStatus
from app.database.database import photo_room, users_db
from app.fsm.fsm import FSM_RENT
from app.keyboards.rent_kb import (
    cancel_rent,
    communication_method,
    how_room,
    rent,
    rental_request,
    send,
    send_contact,
)
from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_RENT
from app.text_creator import TextCreator

router = Router()


# Хендлер чтобы поймать ID фоток
# @router.message(F.photo)
# async def photo(message: Message):
#    print(message.photo[2].file_id)


# Хендлер на кнопку меню 'Аренда'
@router.message(F.text == LEXICON_MENU_BUTTONS['rent'])
async def rent_button(message: Message):
    await message.answer(text=LEXICON_RENT['rent'])
    if photo_room:
        await message.answer_media_group(media=photo_room)
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
@router.callback_query(F.data == 'repeat_request', StateFilter(FSM_RENT.send_rent))
@router.callback_query(F.data == 'rental_request')
async def rental_request_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON_RENT['telephone'], reply_markup=send_contact()
    )
    await state.set_state(FSM_RENT.enter_telephone)


# Хендлер на введенный номер телефона или на присланный контакт,
# переводит в состояние ожидания выбора способа связи
@router.message(StateFilter(FSM_RENT.enter_telephone))
@router.message(F.contact, StateFilter(FSM_RENT.enter_telephone))
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
        await state.set_state(FSM_RENT.how_contact)
    else:
        await message.answer(
            text=f'{LEXICON_RENT["not_telephone"]}\n\n' f'{LEXICON_RENT["breaking"]}',
            reply_markup=cancel_rent(),
        )


# Хендлер на кнопки выбора способа связи,
# переводит в состояние ожидания ввода даты
@router.callback_query(
    StateFilter(FSM_RENT.how_contact), F.data.in_(['call', 'telegram', 'whatsapp'])
)
async def how_contact_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.delete()  # Удалить сообщение с кнопками
    await callback.message.answer(
        text=f'Ты выбрал - {LEXICON_RENT[callback.data]}\n\n' f'{LEXICON_RENT["date"]}'
    )
    await state.set_state(FSM_RENT.date)


# Хендлер будет срабатывать, если во время выбора способа связи
# будет отправлено что-то некорректное
@router.message(StateFilter(FSM_RENT.how_contact))
async def warning_not_contact(message: Message):
    await message.answer(
        text=f'{LEXICON_RENT["not_contact"]}\n\n' f'{LEXICON_RENT["breaking"]}',
        reply_markup=cancel_rent(),
    )


# Хендлер на введенную дату,
# переводит в состояние ожидания ввода мероприятия
@router.message(StateFilter(FSM_RENT.date))
async def date_sent(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer(text=LEXICON_RENT['event'])
    await state.set_state(FSM_RENT.event)


# Хендлер на введенное мероприятие,
# переводит в состояние ожидания ввода количества человек
@router.message(StateFilter(FSM_RENT.event))
async def event_sent(message: Message, state: FSMContext):
    await state.update_data(event=message.text)
    await message.answer(text=LEXICON_RENT['how_people'])
    await state.set_state(FSM_RENT.how_people)


# Хендлер на введенное количество человек,
# переводит в состояние ожидания выбора количества залов
@router.message(StateFilter(FSM_RENT.how_people))
async def how_people_sent(message: Message, state: FSMContext):
    text = message.text
    if text.isdigit():
        await state.update_data(how_people=message.text)
        await message.answer(text=LEXICON_RENT['how_room'], reply_markup=how_room())
        await state.set_state(FSM_RENT.how_room)
    else:
        await message.answer(
            text=f'{LEXICON_RENT["not_people"]}\n\n' f'{LEXICON_RENT["breaking"]}',
            reply_markup=cancel_rent(),
        )


# Хендлер на кнопки выбора количества залов,
# завершает формирование заявки
@router.callback_query(StateFilter(FSM_RENT.how_room), F.data.in_(['one', 'two']))
async def how_room_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(how_room=LEXICON_RENT[callback.data])
    await callback.message.delete()  # Удалить сообщение с кнопками

    id = callback.from_user.id
    data = await state.get_data()
    await state.clear()

    # Формирование сообщения заявки
    text = TextCreator.create_text_rent(users_db, id, mode=PictureStatus.RENT, **data)

    await callback.message.answer(
        text=f'Ты выбрал - {LEXICON_RENT[callback.data]}\n\n'
        f'{LEXICON_RENT["finish"]}\n\n'
        f'{text}',
        reply_markup=send(),
    )
    await state.set_state(FSM_RENT.send_rent)
    await state.update_data(text=text)


# Хендлер будет срабатывать, если во время выбора количества залов
# будет отправлено что-то некорректное
@router.message(StateFilter(FSM_RENT.how_room))
async def warning_not_room(message: Message):
    await message.answer(
        text=f'{LEXICON_RENT["not_room"]}\n\n' f'{LEXICON_RENT["breaking"]}',
        reply_markup=cancel_rent(),
    )


# Хендлер на кнопку 'Отправить'
@router.callback_query(StateFilter(FSM_RENT.send_rent), F.data == 'send')
async def send_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer(text=LEXICON_RENT['sending'])
    # Отправка пользователю данных заявки
    await callback.message.answer(text=f'{data["text"]}')
    # Отправка заявки в чат с админами
    await bot.send_message(chat_id=config.tg_bot.admin_id, text=f'{data["text"]}')
    await state.clear()
