from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


class MastodonPostClick:
    mastodon_api = ...

    async def main(
        self, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Mastodon")
