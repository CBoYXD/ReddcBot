from dataclasses import dataclass

from environs import Env

env = Env()
env.read_env(".env")


@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]


def get_config() -> Config:
    return Config(
        bot_token=env.str("BOT_TOKEN"),
        admin_ids=[int(id) for id in env.list("ADMIN_IDS")],
    )
