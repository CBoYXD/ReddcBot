from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from ....filters import AdminFilter
from ....misc.states import AdminState
from .funcs import ClickFuncs

admin_dialog = Dialog(
    Window(
        Const("Choose network"),
        Row(
            Button(
                Const("Reddit"), id="post_reddit", on_click=ClickFuncs.post.reddit.main
            ),
            Button(
                Const("Lemmy"), id="post_lemmy", on_click=ClickFuncs.post.lemmy.main
            ),
        ),
        Row(
            Button(
                Const("Mastodon"),
                id="post_mastodon",
                on_click=ClickFuncs.post.mastodon.main,
            ),
            Button(
                Const("Youtube"), id="post_yt", on_click=ClickFuncs.post.youtube.main
            ),
        ),
        Row(
            Button(
                Const("Hacker News"),
                id="post_hack_news",
                on_click=ClickFuncs.post.hack_news.main,
            ),
            Button(
                Const("Lobster"),
                id="post_lobster",
                on_click=ClickFuncs.post.lobster.main,
            ),
        ),
        state=AdminState.posts.choose_network,
    ),
)
admin_dialog.callback_query.filter(AdminFilter())
