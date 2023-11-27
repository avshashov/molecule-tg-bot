import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu


# Логирование
logger = logging.getLogger(__name__)

async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Печать в консоль информации о начале запуска бота
    logger.info('Starting bot')

    # Загрузка конфига
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    # Меню бота
    await set_main_menu(bot)

    # Регистрация роутеров
    dp.include_router(user_handlers.router)

    # Запуск поллинга
    # Можно пропустить накопившиеся апдейты пока бот был не в сети
    #await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
