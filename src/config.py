from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from os import getenv


class BotSettings(BaseModel):
    token: str
    admin_ids: list[int]


"""
class RedisSettings(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str
"""


class Config(BaseSettings):
    bot: BotSettings
    # redis: RedisSettings
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=getenv("ENV_FILE", None)
    )


@lru_cache
def get_config() -> Config:
    return Config()


"""
def get_redis_engine(
    db_config: RedisSettings = get_config().redis,
) -> Redis:
    return Redis(
        host=db_config.host,
        port=db_config.port,
        db=db_config.name,
        password=db_config.password,
        username=db_config.user,
    )
"""
