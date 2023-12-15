import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import config
from handlers import menu_handlers, set_user_name, about_project, rent

from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_SET_MENU

from aiogram.fsm.storage.memory import MemoryStorage

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
        format='%(filename)s:%(lineno)d #%(levelname)-8s ' '[%(asctime)s] - %(name)s - %(message)s'
    )

    # Печать в консоль информации о начале запуска бота
    logger.info('Starting bot')

    # Загрузка конфига
    #config: Config = load_config()

    # Инициализация хранилища (MemoryStorage) Нужен Redis?
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # Меню бота
    await set_main_menu(bot)

    # Регистрация роутеров
    dp.include_router(menu_handlers.router)
    dp.include_router(set_user_name.router)
    dp.include_router(about_project.router)
    dp.include_router(rent.router)

    # Запуск поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
