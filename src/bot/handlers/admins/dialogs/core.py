from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from ....filters import AdminFilter
from ....misc.states import AdminState
from .post import PostClick

admin_dialog = Dialog(
    Window(
        Const("Choose network"),
        Row(
            Button(Const("Reddit"), id="post_reddit", on_click=PostClick.reddit),
            Button(Const("Lemmy"), id="post_lemmy", on_click=PostClick.lemmy),
        ),
        Row(
            Button(Const("Mastodon"), id="post_mastodon", on_click=PostClick.mastodon),
            Button(Const("Youtube"), id="post_yt", on_click=PostClick.yt),
        ),
        Row(
            Button(
                Const("Hacker News"),
                id="post_hack_news",
                on_click=PostClick.hacker_news,
            ),
            Button(Const("Lobster"), id="post_lobster", on_click=PostClick.losbter),
        ),
        state=AdminState.posts.choose,
    )
)
admin_dialog.callback_query.filter(AdminFilter())
