from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.admin.common import admin_panel_kb
from app.handlers.admin.rent import router as rent_router
from app.handlers.admin.about_project import router as about_project_router


router = Router()
router.include_routers(rent_router, about_project_router)


@router.message(Command(commands='admin'))
async def admin_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f'Панель администратора.'
             f'\n\nДля изменения наполнения конкретного раздела выбери кнопку ниже:',
        reply_markup=admin_panel_kb(),
    )
