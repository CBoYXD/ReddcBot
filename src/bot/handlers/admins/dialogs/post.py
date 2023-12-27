from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from ....web.reddit.api import RedditAPI


class PostClick:
    reddit_api = RedditAPI()

    @classmethod
    async def reddit(
        cls, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Reddit")

    @classmethod
    async def lemmy(
        cls, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Lemmy")

    @classmethod
    async def mastodon(
        cls, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Mastodon")

    @classmethod
    async def yt(cls, callback: CallbackQuery, button: Button, manager: DialogManager):
        await callback.answer("Youtube")

    @classmethod
    async def losbter(
        cls, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Losbter")

    @classmethod
    async def hacker_news(
        cls, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Hacker News")
