from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class TgBot(BaseModel):
    token: str
    admin_group_id: int


class DatabaseConfig(BaseModel):
    dbms: str
    driver: str
    host: str
    port: int
    user: str
    password: str
    database: str
    echo_db: bool


class SchedulerConfig(BaseModel):
    trigger: str
    day: str
    hour: int
    minute: int


class Config(YamlBaseSettings):
    tg_bot: TgBot
    db: DatabaseConfig
    scheduler: SchedulerConfig

    model_config = SettingsConfigDict(yaml_file='config.yaml')


config = Config()
