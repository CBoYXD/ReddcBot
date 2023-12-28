from dataclasses import dataclass
from datetime import datetime, timedelta

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

    def __convert_time(self, time_delta: timedelta):
        seconds = round(time_delta.total_seconds())
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24
        if days != 0:
            return f"{days} days ago"
        if hours != 0:
            if minutes != 0:
                return f"{hours} hours and {minutes-(hours*60)} minutes ago"
            else:
                return f"{hours} hours ago"
        if minutes != 0:
            if seconds != 0:
                return f"{minutes} minutes and {seconds - (seconds*60)} seconds ago"
            else:
                return f"{seconds} seconds ago"

    def __str__(self) -> str:
        from_time_stamp = datetime.fromtimestamp(self.created_at)
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
            + Bold(
                "⏳Created at⏳: {created_at} ({time_ago})\n\n".format(
                    created_at=from_time_stamp,
                    time_ago=self.__convert_time(datetime.utcnow() - from_time_stamp),
                )
            ).as_html()
            + HashTag(self.subreddit.tag).as_html()
            + ", "
            + HashTag("#" + self.subreddit.id).as_html()
        )


class RedditAPIException(Exception):
    pass
