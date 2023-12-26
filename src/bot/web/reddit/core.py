from dataclasses import dataclass
from typing import Optional


@dataclass
class SubReddit:
    name: str
    id: str
    tag: str
    reddit_tag: str
    subscribers: int


@dataclass
class Post:
    link: str
    id: str
    title: str
    author: str
    post_type: str  # Hot, New, Best, Top, Rising, etc.
    topic: Optional[str]
    subreddit: SubReddit
    upvote_ratio: float
    created_at: int
    score: int
    comments_num: int
    is_video: bool
    media_only: bool
    over_18: bool


class RedditAPIException(Exception):
    pass


async def check_subreddits(subreddits: list[str]):
    ...
