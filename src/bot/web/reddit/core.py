from dataclasses import dataclass

from aiogram.utils.formatting import Bold, HashTag, TextLink


@dataclass
class SubReddit:
    name: str
    id: str
    tag: str
    subscribers: int


@dataclass
class Post:
    link: str
    id: str
    title: str
    author: str
    post_type: str  # Hot, New, Best, Top, Rising, etc.
    subreddit: SubReddit
    upvote_ratio: float
    created_at: int
    score: int
    comments_num: int
    is_video: bool
    media_only: bool
    over_18: bool

    def __str__(self) -> str:
        over_18 = (
            ""
            if self.over_18 is False
            else Bold(f"🔞 Over 18 🔞: {self.over_18}\n\n").as_html()
        )
        return (
            Bold(f"{self.post_type}🔥 from {self.subreddit.name}\n\n").as_html()
            + f"{Bold('🔍 Title 🔍: ').as_html()}{TextLink(self.title, url=self.link).as_html()}\n\n"
            + Bold(f"✍️ Author ✍️: {self.author}\n\n").as_html()
            + Bold(f"💬 Comments Num 💬: {self.comments_num}\n\n").as_html()
            + Bold(f"⭐️ Score ⭐️: {self.score}\n\n").as_html()
            + Bold(f"👍 Upvote Ratio 👎: {self.upvote_ratio}\n\n").as_html()
            + Bold(f"📱 Media Only 📱: {self.media_only}\n\n").as_html()
            + Bold(f"🎥 Video 🎥: {self.is_video}\n\n").as_html()
            + over_18
            + HashTag(self.subreddit.tag).as_html()
            + ", "
            + HashTag("#" + self.subreddit.id).as_html()
        )


class RedditAPIException(Exception):
    pass
