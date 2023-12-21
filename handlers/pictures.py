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
    send_correct,
    cancel_picture,
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
    await callback.message.edit_text(
        text=LEXICON_PICTURES['buy_ready_description'], reply_markup=buy_ready()
    )
    await callback.answer()


# Хендлер на кнопку 'Свяжитесь со мной' и кнопку 'Исправить' а также на кнопку 'Заказать картину'
@router.callback_query(F.data == 'correct', StateFilter(FSM_PICTURE.send))
@router.callback_query(F.data == 'contact_me')
@router.callback_query(F.data == 'order_painting')
async def contact_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_PICTURES['how_contact_2'], reply_markup=method_contact())
    await callback.answer()
    if callback.data in ['contact_me', 'correct']:
        await callback.message.edit_text(text=LEXICON_PICTURES['pictures'], reply_markup=pictures())
    elif callback.data == 'order_painting':
        await state.set_state(FSM_PICTURE.how_contact_order)


# Хендлер на кнопку "Отменить"
@router.callback_query(F.data == 'cancel_button_pictures', ~StateFilter(default_state))
async def cancel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_PICTURES['cancel_process'], reply_markup=pictures())
    await state.clear()
    await callback.answer()


# Хендлер на кнопки 'Звонок', 'whatsapp', 'telegram'
@router.callback_query(
    StateFilter(FSM_PICTURE.how_contact_buy_ready, FSM_PICTURE.how_contact_order),
    F.data.in_(['call', 'telegram', 'whatsapp']),
)
async def how_contact(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.answer(text=LEXICON_PICTURES['number'], reply_markup=send_contact())
    if FSM_PICTURE.how_contact_buy_ready == await state.get_state():
        await state.set_state(FSM_PICTURE.enter_telephone_buy_ready)
    elif FSM_PICTURE.how_contact_order == await state.get_state():
        await state.set_state(FSM_PICTURE.enter_telephone_order)


# Хендлер будет срабатывать, если во время выбора способа связи
# будет отправлено что-то некорректное
@router.message(StateFilter(FSM_PICTURE.how_contact_buy_ready))
async def warning_not_contact(message: Message):
    await message.answer(
        text=f'{LEXICON_RENT["not_contact"]}\n\n' f'{LEXICON_PICTURES["breaking"]}',
        reply_markup=method_contact(),
    )


# Хендлер на кнопку 'email'
@router.callback_query(
    StateFilter(FSM_PICTURE.how_contact_buy_ready, FSM_PICTURE.how_contact_order), F.data == 'email'
)
async def email_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_PICTURES['enter_email'])
    if FSM_PICTURE.how_contact_buy_ready == await state.get_state():
        await state.set_state(FSM_PICTURE.enter_email_buy_ready)
    elif FSM_PICTURE.how_contact_order == await state.get_state():
        await state.set_state(FSM_PICTURE.enter_email_order)


# Хендлер на введенный номер телефона, email или на присланный контакт в состояниях -
# Заказ картины и Купить готовую картину
# Формирует сообщение для 2 вариантов и сразу отправляет при состоянии - Купить готовую,
# либо при состоянии - Заказ переводит в дальнейшие состояния (вопросы)
@router.message(StateFilter(FSM_PICTURE.enter_email_buy_ready, FSM_PICTURE.enter_email_order))
@router.message(StateFilter(FSM_PICTURE.enter_telephone_buy_ready, FSM_PICTURE.enter_telephone_order))
@router.message(
    F.contact, StateFilter(FSM_PICTURE.enter_telephone_buy_ready, FSM_PICTURE.enter_telephone_order)
)
async def contact_sent(message: Message, state: FSMContext):
    text = ''
    id = message.from_user.id
    # Если состояние - ввод телефона
    if (
        FSM_PICTURE.enter_telephone_buy_ready == await state.get_state()
        or FSM_PICTURE.enter_telephone_order == await state.get_state()
    ) and ((message.text and message.text.isdigit()) or message.contact):
        await message.answer(text='👍', reply_markup=ReplyKeyboardRemove())
        if message.text:
            await state.update_data(enter_telephone=message.text)
        elif message.contact:
            await state.update_data(enter_telephone=message.contact.phone_number)

        data = await state.get_data()

        # Формирование сообщения если указан телефон
        text = f'''Заказ: Готовая картина
Имя: {users_db[id]["name"]}
Телефон: {data["enter_telephone"]}
Способ связи: {data["how_contact"]}\n'''

    # Если состояние - ввод email (Купить готовую)
    if FSM_PICTURE.enter_email_buy_ready == await state.get_state():
        # Формирование сообщения
        text = f'''Заказ: Готовая картина
Имя: {users_db[id]["name"]}
E-mail: {message.text}'''

    # Если состояние - ввод email (Заказ)
    if FSM_PICTURE.enter_email_order == await state.get_state():
        await state.update_data(enter_email=message.text)
        await message.answer(text=LEXICON_PICTURES['addressee'])
        await state.set_state(FSM_PICTURE.for_whom)

    # Если сообщение сформировано и состояния - Купить готовую
    if text and (
        FSM_PICTURE.enter_telephone_buy_ready == await state.get_state()
        or FSM_PICTURE.enter_email_buy_ready == await state.get_state()
    ):
        await message.answer(
            text=f'Проверь данные -\n\n{text}\nЕсли верно - жми "Отправить", если нет - "Исправить"',
            reply_markup=send_correct(),
        )
        await state.clear()
        await state.set_state(FSM_PICTURE.send)
        await state.update_data(text=text)

    # Если текст сформирован и состояние - Заказ
    elif text and FSM_PICTURE.enter_telephone_order == await state.get_state():
        await state.clear()
        await state.update_data(text=text)
        await message.answer(text=LEXICON_PICTURES['addressee'])
        await state.set_state(FSM_PICTURE.for_whom)

    # Если пользователь указал какую-то дичь вместо телефона  и состояния - ввод телефона
    elif text == '' and (
        FSM_PICTURE.enter_telephone_buy_ready == await state.get_state()
        or FSM_PICTURE.enter_telephone_order == await state.get_state()
    ):
        await message.answer(
            text=f'{LEXICON_RENT["not_telephone"]}\n\n' f'{LEXICON_PICTURES["breaking"]}',
            reply_markup=cancel_picture(),
        )


# Хендлер на вопрос 'Для кого картина'
@router.message(StateFilter(FSM_PICTURE.for_whom))
async def for_whom(message: Message, state: FSMContext):
    await state.update_data(for_whom=message.text)
    await message.answer(text=LEXICON_PICTURES['event'])
    await state.set_state(FSM_PICTURE.event)


# Хендлер на вопрос 'По какому случаю'
@router.message(StateFilter(FSM_PICTURE.event))
async def event(message: Message, state: FSMContext):
    await state.update_data(event=message.text)
    await message.answer(text=LEXICON_PICTURES['size'])
    await state.set_state(FSM_PICTURE.size)


# Хендлер на вопрос 'Размер картины'
@router.message(StateFilter(FSM_PICTURE.size))
async def size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer(text=LEXICON_PICTURES['mood'])
    await state.set_state(FSM_PICTURE.mood)


# Хендлер на вопрос 'Настроение'
@router.message(StateFilter(FSM_PICTURE.mood))
async def mood(message: Message, state: FSMContext):
    await state.update_data(mood=message.text)
    await message.answer(text=LEXICON_PICTURES['color'])
    await state.set_state(FSM_PICTURE.color)


# Хендлер на вопрос 'Цветовая гамма'
@router.message(StateFilter(FSM_PICTURE.color))
async def color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)

    data = await state.get_data()

    if data["text"]:
    # Формирование сообщения если указан телефон
        text = data["text"] + f'''\nКому картина: {data["for_whom"]}
Событие: {data["event"]}
Размер: {data["size"]}
Настроение: {data["mood"]}
Цвета: {data["color"]}\n'''

    await message.answer(
            text=f'Проверь данные -\n\n{text}\nЕсли верно - жми "Отправить", если нет - "Исправить"(Ответить заново)',
            reply_markup=send_correct(),
        )
    await state.clear()
    await state.update_data(text=text)
    await state.set_state(FSM_PICTURE.send)


# Хендлер на кнопку 'Отправить'
@router.callback_query(StateFilter(FSM_PICTURE.send), F.data == 'send_contact')
async def send_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer(text=LEXICON_PICTURES['finish_2'])
    # Отправка пользователю данных заявки
    await callback.message.answer(text=f'{data["text"]}')
    # Отправка заявки в чат с админами
    await bot.send_message(chat_id=config.tg_bot.admin_ids[0], text=f'{data["text"]}')
    await callback.answer()
    await state.clear()
