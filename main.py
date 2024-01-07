import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from src.bot.config import Config, get_config
from src.bot.handlers import routers_list
from src.bot.service import broadcast
from src.web.reddit.api import RedditAPI


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def on_startup(bot: Bot, admin_id: str) -> None:
    await broadcast(bot, admin_id, "Бот був запущений")


async def main() -> None:
    config: Config = get_config()
    dp = Dispatcher(reddit=RedditAPI())
    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    setup_logging()
    dp.include_routers(*routers_list)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot, config.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
