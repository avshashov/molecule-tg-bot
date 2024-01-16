from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from app.constants import PictureStatus
from app.fsm.fsm import FSMPicture
from app.keyboards.menu_kb import menu_kb
from app.keyboards.pictures_kb import (
    buy_ready,
    cancel_picture,
    method_contact,
    pictures,
    send_correct,
    skip,
)
from app.keyboards.rent_kb import send_contact
from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_PICTURES, LEXICON_RENT
from app.text_creator import TextCreator

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


# Хендлер на кнопку 'Свяжитесь со мной' и 'Заказать картину'
@router.callback_query(F.data.in_(['contact_me', 'order_painting']))
async def contact_button(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'contact_me':
        await callback.message.edit_text(
            text=LEXICON_PICTURES['how_contact_buy'],
            reply_markup=method_contact(picture_is_ready=True),
        )
        await state.set_state(FSMPicture.how_contact_buy_ready)
    elif callback.data == 'order_painting':
        await callback.message.edit_text(
            text=LEXICON_PICTURES['how_contact_order'],
            reply_markup=method_contact(picture_is_ready=False),
        )
        await state.set_state(FSMPicture.how_contact_order)


# Хендлер на кнопку "Отменить" - выводит в меню картины
@router.callback_query(
    F.data.startswith('cancel_button_pictures'), ~StateFilter(default_state)
)
async def cancel_button(callback: CallbackQuery, state: FSMContext):
    if callback.data.endswith('True'):
        await callback.message.edit_text(
            text=LEXICON_PICTURES['cancel_process'], reply_markup=buy_ready()
        )
    else:
        await callback.message.edit_text(
            text=LEXICON_PICTURES['pictures'], reply_markup=pictures()
        )
    await state.clear()


# Хендлер на кнопку "Назад" - Возвращает на шаг назад
@router.callback_query(F.data == 'back_pictures')
async def back_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_PICTURES['pictures'], reply_markup=pictures()
    )


# Хендлер на кнопки 'Звонок', 'whatsapp', 'telegram'
@router.callback_query(
    StateFilter(FSMPicture.how_contact_buy_ready, FSMPicture.how_contact_order),
    F.data.in_(['call', 'telegram', 'whatsapp']),
)
async def how_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(how_contact=LEXICON_RENT[callback.data])
    await callback.message.answer(
        text=LEXICON_PICTURES['number'], reply_markup=send_contact()
    )
    if FSMPicture.how_contact_buy_ready == await state.get_state():
        await state.set_state(FSMPicture.enter_telephone_buy_ready)
    elif FSMPicture.how_contact_order == await state.get_state():
        await state.set_state(FSMPicture.enter_telephone_order)


# Хендлер будет срабатывать, если во время выбора способа связи
# будет отправлено что-то некорректное
@router.message(
    StateFilter(FSMPicture.how_contact_buy_ready, FSMPicture.how_contact_order)
)
async def warning_not_contact(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FSMPicture.how_contact_buy_ready:
        keyboard = method_contact(picture_is_ready=True)
    else:
        keyboard = method_contact(picture_is_ready=False)
    await message.answer(
        text=f'{LEXICON_RENT["not_contact"]}\n\n' f'{LEXICON_PICTURES["breaking"]}',
        reply_markup=keyboard,
    )


# Хендлер на кнопку 'email'
@router.callback_query(
    StateFilter(FSMPicture.how_contact_buy_ready, FSMPicture.how_contact_order),
    F.data == 'email',
)
async def email_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_PICTURES['enter_email'])
    if FSMPicture.how_contact_buy_ready == await state.get_state():
        await state.set_state(FSMPicture.enter_email_buy_ready)
    elif FSMPicture.how_contact_order == await state.get_state():
        await state.set_state(FSMPicture.enter_email_order)


# Хендлер на введенный email - отправка данных админам
@router.message(
    StateFilter(FSMPicture.enter_email_buy_ready, FSMPicture.enter_email_order)
)
async def email_process(message: Message, state: FSMContext, session: AsyncSession):
    if FSMPicture.enter_email_buy_ready == await state.get_state():
        await state.update_data(enter_email=message.text)
        id = message.from_user.id
        data = await state.get_data()
        text = await TextCreator.create_text_ready(session, id, mode='ready', **data)
        await message.answer(
            text=f'Проверь данные -\n\n{text}\n\nЕсли верно - жми "Отправить", если нет - "Исправить"',
            reply_markup=send_correct(),
        )
        await state.clear()
        await state.set_state(FSMPicture.send_buy_ready)
        await state.update_data(text=text)
    elif FSMPicture.enter_email_order == await state.get_state():
        await state.update_data(enter_email=message.text)
        await message.answer(text=LEXICON_PICTURES['addressee'], reply_markup=skip())
        await state.set_state(FSMPicture.for_whom)


# Хендлер на введенный номер телефона или на присланный контакт
@router.message(
    StateFilter(
        FSMPicture.enter_telephone_buy_ready, FSMPicture.enter_telephone_order
    )
)
async def contact_sent(message: Message, state: FSMContext, session: AsyncSession):
    if (message.text and message.text.isdigit()) or message.contact:
        await message.answer(
            text='👍', reply_markup=ReplyKeyboardRemove()
        )  # Удалить кнопку <Отправить контакт>
        if message.text:
            await state.update_data(enter_telephone=message.text)
        elif message.contact:
            await state.update_data(enter_telephone=message.contact.phone_number)
        if FSMPicture.enter_telephone_buy_ready == await state.get_state():
            # формирование сообшения - отправка данных админам
            id = message.from_user.id
            data = await state.get_data()
            text = await TextCreator.create_text_ready(
                session, id, mode=PictureStatus.READY, **data
            )
            await message.answer(
                text=f'Проверь данные -\n\n{text}\n\nЕсли верно - жми "Отправить", если нет - "Исправить"',
                reply_markup=send_correct(),
            )
            await state.clear()
            await state.set_state(FSMPicture.send_buy_ready)
            await state.update_data(text=text)

        elif FSMPicture.enter_telephone_order == await state.get_state():
            await message.answer(
                text=LEXICON_PICTURES['addressee'], reply_markup=skip()
            )
            await state.set_state(FSMPicture.for_whom)
    else:
        await message.answer(
            text=f'{LEXICON_RENT["not_telephone"]}\n\n'
            f'{LEXICON_PICTURES["breaking"]}',
            reply_markup=cancel_picture(),
        )


# Хендлер на вопрос 'Для кого картина'
@router.message(StateFilter(FSMPicture.for_whom))
async def for_whom(message: Message, state: FSMContext):
    if message.text != LEXICON_PICTURES['skip']:
        await state.update_data(for_whom=message.text)
    await message.answer(text=LEXICON_PICTURES['event'], reply_markup=skip())
    await state.set_state(FSMPicture.event)


# Хендлер на вопрос 'По какому случаю'
@router.message(StateFilter(FSMPicture.event))
async def event(message: Message, state: FSMContext):
    if message.text != LEXICON_PICTURES['skip']:
        await state.update_data(event=message.text)
    await message.answer(text=LEXICON_PICTURES['size'], reply_markup=skip())
    await state.set_state(FSMPicture.size)


# Хендлер на вопрос 'Размер картины'
@router.message(StateFilter(FSMPicture.size))
async def size(message: Message, state: FSMContext):
    if message.text != LEXICON_PICTURES['skip']:
        await state.update_data(size=message.text)
    await message.answer(text=LEXICON_PICTURES['mood'], reply_markup=skip())
    await state.set_state(FSMPicture.mood)


# Хендлер на вопрос 'Настроение'
@router.message(StateFilter(FSMPicture.mood))
async def mood(message: Message, state: FSMContext):
    if message.text != LEXICON_PICTURES['skip']:
        await state.update_data(mood=message.text)
    await message.answer(text=LEXICON_PICTURES['color'], reply_markup=skip())
    await state.set_state(FSMPicture.color)


# Хендлер на вопрос 'Цветовая гамма' - проверка всех введенных данных пользователем
@router.message(StateFilter(FSMPicture.color))
async def color(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer(
        text='Благодарю за ответы ☑️', reply_markup=ReplyKeyboardRemove()
    )
    if message.text != LEXICON_PICTURES['skip']:
        await state.update_data(color=message.text)
    id = message.from_user.id
    data = await state.get_data()
    text = await TextCreator.create_text_order(
        session, id, mode=PictureStatus.ORDER, **data
    )
    await message.answer(
        text=f'Проверь данные -\n\n{text}\n\nЕсли верно - жми "Отправить", если нет - "Исправить"(Ответить заново)',
        reply_markup=send_correct(),
    )
    await state.clear()
    await state.update_data(text=text)
    await state.set_state(FSMPicture.send_order)


# Хендлер на кнопку 'Отправить'
@router.callback_query(
    F.data == 'send_contact',
    StateFilter(FSMPicture.send_buy_ready, FSMPicture.send_order),
)
async def send_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer(text=LEXICON_RENT['sending'])
    # Отправка пользователю данных заявки
    await callback.message.answer(text=f'{data["text"]}', reply_markup=menu_kb())
    # Отправка заявки в чат с админами
    await bot.send_message(chat_id=config.tg_bot.admin_group_id, text=f'{data["text"]}')
    await state.clear()


# Хендлер на нопку 'Исправить' - предлагает ответить на вопросы еще раз
@router.callback_query(
    F.data == 'correct', StateFilter(FSMPicture.send_buy_ready, FSMPicture.send_order)
)
async def correct_button(callback: CallbackQuery, state: FSMContext):
    if FSMPicture.send_buy_ready == await state.get_state():
        await callback.message.edit_text(
            text=LEXICON_PICTURES['how_contact_buy'],
            reply_markup=method_contact(picture_is_ready=True),
        )
        await state.clear()
        await state.set_state(FSMPicture.how_contact_buy_ready)
    elif FSMPicture.send_order == await state.get_state():
        await callback.message.edit_text(
            text=LEXICON_PICTURES['how_contact_order'],
            reply_markup=method_contact(picture_is_ready=False),
        )
        await state.clear()
        await state.set_state(FSMPicture.how_contact_order)
