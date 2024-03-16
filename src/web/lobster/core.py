from dataclasses import dataclass
from datetime import datetime


@dataclass
class Post:
    link: str
    title: str
    id: str
    news_url: str
    score: int
    comment_count: int
    tags: list[str]
    comments_url: str
    user_is_author: bool
    created_at: datetime


class LobsterAPIException(Exception):
    pass
