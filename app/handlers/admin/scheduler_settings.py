from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import CRUDPicture
from app.fsm.fsm import FSMAdminPicture
from app.keyboards.admin.common_kb import admin_panel_kb
from app.keyboards.admin.scheduler_kb import (
    back_pictures_menu,
    cancel_kb,
    confirm_delete_picture_kb,
    list_of_current_pictures_kb,
    open_picture_kb,
    picture_menu_kb,
)
from app.schemas import PictureCreate, PictureUpdate

router = Router()


@router.callback_query(F.data == 'admin pictures')
async def admin_pictures_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Меню настройки картин для рассылки пользователям',
        reply_markup=picture_menu_kb(),
    )


@router.callback_query(F.data == 'back admin panel from pictures')
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=f'Панель администратора.'
        f'\n\nДля изменения наполнения конкретного раздела выбери кнопку ниже:',
        reply_markup=admin_panel_kb(),
    )


@router.callback_query(F.data == 'add picture')
async def add_new_picture(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text=f'Загрузи картину как обычное фото (не документ)',
        reply_markup=cancel_kb(),
    )
    await state.set_state(FSMAdminPicture.upload_picture)


@router.message(F.photo, StateFilter(FSMAdminPicture.upload_picture))
async def send_picture(message: Message, state: FSMContext):
    await state.update_data(picture_id=message.photo[2].file_id)
    await message.answer(
        text='Введи короткое название к картине, '
        'это название будет использоваться в блоке редактирования картин.'
        '\nПользователь этого названия не увидит.'
        '\n\nНапример: Ухи',
        reply_markup=cancel_kb(),
    )
    await state.set_state(FSMAdminPicture.enter_picture_title)


@router.message(~(F.text == 'Отмена'), StateFilter(FSMAdminPicture.enter_picture_title))
async def get_picture_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer(
        text='Введи описание к картине, которое будет использоваться в рассылке',
        reply_markup=cancel_kb(),
    )
    await state.set_state(FSMAdminPicture.enter_picture_description)


@router.message(
    ~(F.text == 'Отмена'), StateFilter(FSMAdminPicture.enter_picture_description)
)
async def get_picture_description(
    message: Message, state: FSMContext, session: AsyncSession
):
    description = message.md_text.strip()
    data = await state.get_data()
    picture = PictureCreate(
        picture_id=data['picture_id'],
        title=data['title'],
        description=description,
    )
    await CRUDPicture.create_picture(session, picture_fields=picture)
    await message.answer(text='Картина добавлена', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text='Меню настройки картин для рассылки пользователям',
        reply_markup=picture_menu_kb(),
    )
    await state.clear()


@router.message(
    F.text == 'Отмена',
    StateFilter(
        FSMAdminPicture.upload_picture,
        FSMAdminPicture.enter_picture_title,
        FSMAdminPicture.enter_picture_description,
    ),
)
async def cancel_add_picture(message: Message, state: FSMContext):
    await message.answer(text='Действие отменено', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text='Меню настройки картин для рассылки пользователям',
        reply_markup=picture_menu_kb(),
    )
    await state.clear()


@router.callback_query(F.data == 'back to list pictures')
@router.callback_query(F.data == 'edit pictures')
async def edit_pictures_menu(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    pictures = await CRUDPicture.get_pictures(session)
    if not pictures:
        await callback.message.delete()
        await callback.message.answer(
            text='Тут пусто, сперва загрузки картины',
            reply_markup=back_pictures_menu(),
        )
        await state.clear()
    else:
        await callback.message.delete()
        await callback.message.answer(
            text='Картины',
            reply_markup=list_of_current_pictures_kb(pictures),
        )
        await state.set_state(FSMAdminPicture.open_picture)


@router.callback_query(F.data == 'back pictures menu')
async def back_to_pictures_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Меню настройки картин для рассылки пользователям',
        reply_markup=picture_menu_kb(),
    )


@router.callback_query(F.data == 'delete picture menu')
async def delete_picture_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=confirm_delete_picture_kb(),
    )


@router.callback_query(F.data == 'cancel delete picture')
async def cancel_delete_picture(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=open_picture_kb(),
    )


@router.callback_query(F.data == 'confirm delete picture')
async def confirm_delete_picture(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    await CRUDPicture.delete_picture(session, id=int(data['picture_id']))
    pictures = await CRUDPicture.get_pictures(session)
    if not pictures:
        await callback.message.delete()
        await callback.message.answer(
            text='Тут пусто, сперва загрузки картины',
            reply_markup=back_pictures_menu(),
        )
        await state.clear()
    else:
        await callback.message.delete()
        await callback.message.answer(
            text='Картины',
            reply_markup=list_of_current_pictures_kb(pictures),
        )
        await state.set_state(FSMAdminPicture.open_picture)


@router.callback_query(F.data == 'change picture title')
async def change_picture_title(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Введи новое название к картине, '
        'это название будет использоваться в блоке редактирования картин.'
        '\nПользователь этого названия не увидит.'
        '\n\nНапример: Ухи',
        reply_markup=cancel_kb(),
    )
    data = await state.get_data()
    await state.set_state(FSMAdminPicture.enter_new_picture_title)
    await state.update_data(**data)


@router.callback_query(F.data == 'change picture description')
async def change_picture_description(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Введи описание к картине, которое будет использоваться в рассылке',
        reply_markup=cancel_kb(),
    )
    data = await state.get_data()
    await state.set_state(FSMAdminPicture.enter_new_picture_description)
    await state.update_data(**data)


@router.message(
    ~(F.text == 'Отмена'),
    StateFilter(
        FSMAdminPicture.enter_new_picture_title,
        FSMAdminPicture.enter_new_picture_description,
    ),
)
async def get_new_picture_title_or_description(
    message: Message, state: FSMContext, session: AsyncSession
):
    current_state = await state.get_state()
    picture_fields = PictureUpdate()
    if current_state == FSMAdminPicture.enter_new_picture_title:
        picture_fields.title = message.text.strip()
    elif current_state == FSMAdminPicture.enter_new_picture_description:
        picture_fields.description = message.md_text.strip()

    data = await state.get_data()
    await state.set_state(FSMAdminPicture.open_picture)
    await state.update_data(**data)
    picture = await CRUDPicture.update_picture(
        session, id=data['picture_id'], picture_fields=picture_fields
    )
    text = f'Заголовок: {picture.title}' f'\n\nОписание: {picture.description}'
    await message.answer(text='Картина обновлена', reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(
        photo=picture.picture_id, caption=text, reply_markup=open_picture_kb()
    )


@router.message(
    F.text == 'Отмена',
    StateFilter(
        FSMAdminPicture.enter_new_picture_title,
        FSMAdminPicture.enter_new_picture_description,
    ),
)
async def cancel_edit_picture_title_or_description(
    message: Message, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    await state.set_state(FSMAdminPicture.open_picture)
    await state.update_data(**data)

    picture = await CRUDPicture.get_picture_by_id(session, id=data['picture_id'])
    text = f'Заголовок: {picture.title}' f'\n\nОписание: {picture.description}'
    await message.answer(text='Действие отменено', reply_markup=ReplyKeyboardRemove())
    # TODO: не работает markdown форматирование через parse_mode=ParseMode.MARKDOWN_V2
    await message.answer_photo(
        photo=picture.picture_id,
        caption=text,
        reply_markup=open_picture_kb(),
    )


@router.callback_query(StateFilter(FSMAdminPicture.open_picture))
async def open_picture(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    picture_id = int(callback.data)
    await state.update_data(picture_id=picture_id)
    picture = await CRUDPicture.get_picture_by_id(session, picture_id)
    await callback.message.delete()
    text = f'Заголовок: {picture.title}' f'\n\nОписание: {picture.description}'
    # TODO: не работает markdown форматирование через parse_mode=ParseMode.MARKDOWN_V2
    await callback.message.answer_photo(
        photo=picture.picture_id, caption=text, reply_markup=open_picture_kb()
    )
