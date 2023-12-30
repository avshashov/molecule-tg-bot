from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    dbms: str
    database: str  # Название базы данных
    host: str  # URL-адрес базы данных
    user: str  # Username пользователя базы данных
    password: str  # Пароль к базе данных
    driver: str
    port: int
    echo_db: bool


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_id: int  # id администратора бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


# Функция, которая будет читать файл .env и возвращать
# экземпляр класса Config

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_id=env('ADMIN_IDS')
        ),
        db=DatabaseConfig(
            dbms=env('dbms'),
            database=env('database'),
            host=env('host'),
            user=env('user'),
            password=env('password'),
            driver=env('driver'),
            port=env('port'),
            echo_db=env('echo_db'))
    )


config: Config = load_config()
