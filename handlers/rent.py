from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RENT, LEXICON_MENU_BUTTONS
from database.database import photo_room, users_db
from keyboards.keyboards import rent, communication_method, how_room, send, menu_kb
from config_data.config import Config, load_config

from aiogram.fsm.context import FSMContext
from fsm.fsm import FSM_RENT
from aiogram.fsm.state import default_state


router = Router()


# Хендлер чтобы поймать ID фоток
#@router.message(F.photo)
#async def photo(message: Message):
#    print(message.photo[2].file_id)


# Хендлер на кнопку меню 'Аренда'
@router.message(F.text == LEXICON_MENU_BUTTONS['rent'])
async def rent_button(message: Message):
    await message.answer(text=LEXICON_RENT['rent'])
    await message.answer_media_group(media=photo_room)
    await message.answer(text='Оставляй заявку, если заинтересовало 👇', reply_markup=rent())


# Хендлер будет срабатывать на команду "/cancel" в любых состояниях, кроме дефолтного
@router.message(F.text == '/cancel', ~StateFilter(default_state))
async def cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RENT['cancel'])
    await state.clear()


# Хендлер будет срабатывать на команду "/cancel" в состоянии по умолчанию
@router.message(F.text =='/cancel', StateFilter(default_state))
async def cancel_default(message: Message):
    await message.answer(text=LEXICON_RENT['cancel_default'])


# Хендлер на кнопку 'Оставить заявку на аренду помещения'
# Устанавливает состояние ввода телефона
@router.callback_query(F.data == 'rental_request')
async def rental_request_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RENT['telephone'])
    await state.set_state(FSM_RENT.enter_telephone)


# Хендлер на введенный номер телефона или на присланный контакт,
# переводит в состояние ожидания выбора способа связи
@router.message(StateFilter(FSM_RENT.enter_telephone))
@router.message(F.contact, StateFilter(FSM_RENT.enter_telephone))
async def telephone_sent(message: Message, state: FSMContext):
    if message.text:
        text = message.text
    if (message.text and text.isdigit()) or message.contact:
        await state.update_data(enter_telephone=message.text)
        await message.answer(text=LEXICON_RENT['how_contact'], reply_markup=communication_method())
        await state.set_state(FSM_RENT.how_contact)
    else:
        await message.answer(text=f'{LEXICON_RENT["not_telephone"]}\n\n'
                                  f'{LEXICON_RENT["breaking"]}')


# Хендлер на кнопки выбора способа связи,
# переводит в состояние ожидания ввода даты
@router.callback_query(StateFilter(FSM_RENT.how_contact),
                       F.data.in_(['call', 'telegram', 'whatsapp']))
async def how_contact_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.delete()  # Удалить сообщение с кнопками
    await callback.message.answer(text=f'Вы выбрали - {LEXICON_RENT[callback.data]}\n\n'
                                       f'{LEXICON_RENT["date"]}')
    await state.set_state(FSM_RENT.date)


# Хендлер будет срабатывать, если во время выбора способа связи
# будет отправлено что-то некорректное
@router.message(StateFilter(FSM_RENT.how_contact))
async def warning_not_contact(message: Message):
    await message.answer(text=f'{LEXICON_RENT["not_contact"]}\n\n'
                              f'{LEXICON_RENT["breaking"]}')


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
        await message.answer(text=f'{LEXICON_RENT["not_people"]}\n\n'
                                  f'{LEXICON_RENT["breaking"]}')


# Хендлер на кнопки выбора количества залов,
# завершает формирование заявки
@router.callback_query(StateFilter(FSM_RENT.how_room),
                       F.data.in_(['one', 'two']))
async def how_room_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(how_room=LEXICON_RENT[callback.data])
    await callback.message.delete()  # Удалить сообщение с кнопками

    id = callback.from_user.id
    data = await state.get_data()
    await state.clear()

    # Формирование сообщения заявки
    text = f'''Имя: {users_db[id]["name"]}\n
Телефон: {data["enter_telephone"]}\n
Способ связи: {data["how_contact"]}\n
Дата: {data["date"]}\n
Мероприятие: {data["event"]}\n
Сколько человек: {data["how_people"]}\n
Залов требуется: {data["how_room"]}'''

    await callback.message.answer(text=f'Вы выбрали - {LEXICON_RENT[callback.data]}\n\n'
                                       f'{LEXICON_RENT["finish"]}\n\n'
                                       f'{text}',
                                       reply_markup=send())
    await state.update_data(text=text)


# Хендлер будет срабатывать, если во время выбора количества залов
# будет отправлено что-то некорректное
@router.message(StateFilter(FSM_RENT.how_room))
async def warning_not_room(message: Message):
    await message.answer(text=f'{LEXICON_RENT["not_room"]}\n\n'
                              f'{LEXICON_RENT["breaking"]}')


# Хендлер на кнопку 'Отправить'
@router.callback_query(F.data == 'send')
async def send_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RENT['sending'])
    data = await state.get_data()
    config: Config = load_config()
    await bot.send_message(chat_id=config.tg_bot.admin_ids[0],
                           text=f'{data["text"]}')
    await state.clear()