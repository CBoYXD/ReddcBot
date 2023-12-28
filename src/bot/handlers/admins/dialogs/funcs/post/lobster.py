from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


class LobsterPostClick:
    lobster_post_click = ...

    async def main(
        self, callback: CallbackQuery, button: Button, manager: DialogManager
    ):
        await callback.answer("Lobster")
