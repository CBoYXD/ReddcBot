from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from .......web.reddit.api import RedditAPI


class RedditPostClick:
    reddit_api = RedditAPI()

    async def main(
        self, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Reddit")
