import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config import config
from app.database.settings import bot_db
from app.handlers import rent, about_project, menu_handlers, pictures, set_user_name

from aiogram.types import BotCommand
from app.lexicon.lexicon_ru import LEXICON_SET_MENU

from aiogram.fsm.storage.memory import MemoryStorage

from app.middlewares import SessionMiddleware

# Логирование
logger = logging.getLogger(__name__)


# Функция настройки меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_SET_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - %(levelname)s - %(message)s'
    )

    # Печать в консоль информации о начале запуска бота
    logger.info('Starting bot')

    # Инициализация хранилища (MemoryStorage) Нужен Redis?
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # Меню бота
    await set_main_menu(bot)

    # Регистрация роутеров
    dp.update.middleware(SessionMiddleware(bot_db.async_session_maker))
    dp.include_router(menu_handlers.router)
    dp.include_router(set_user_name.router)
    dp.include_router(about_project.router)
    dp.include_router(rent.router)
    dp.include_router(pictures.router)

    # Запуск поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
