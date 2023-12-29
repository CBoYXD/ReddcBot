from dataclasses import dataclass
from datetime import datetime, timedelta

from aiogram.utils.formatting import Bold, HashTag, TextLink


@dataclass
class SubReddit:
    name: str
    title: str
    link: str
    lang: str
    id: str
    type: str
    over_18: bool
    created_at: datetime

    def __str__(self) -> str:
        over_18 = (
            ""
            if self.over_18 is False
            else Bold(f"🔞 Over 18 🔞: {self.over_18}\n\n").as_html()
        )
        return (
            Bold("👥Subreddit👥: ").as_html()
            + TextLink(self.name, self.link).as_html()
            + "\n\n"
            + Bold(f"🆔: {self.id}").as_html()
            + "\n\n"
            + Bold(f"🔍 Title 🔍: {self.title}")
            + Bold(f"🗣 Language 💬 {self.language}").as_html()
            + "\n\n"
            + Bold(f"🧩 Type 🧩: {self.type}")
            + "\n\n"
            + over_18
            + Bold(f"⏳ Created UTC ⏳: {str(self.created_utc)}").as_html()
            + "\n\n"
        )


@dataclass
class Redditor:
    name: str
    id: str
    link: str
    comment_karma: int
    link_karma: int
    accept_chats: bool
    accept_pms: bool
    accept_followers: bool
    verified: bool
    created_utc: datetime

    def __str__(self) -> str:
        return (
            Bold("👤 User 👤: ").as_html()
            + TextLink(self.name, self.link).as_html()
            + "\n\n"
            + Bold(f"🆔: {self.id}").as_html()
            + "\n\n"
            + Bold(f"🔮 Comment Karma 💬: {self.comment_karma}").as_html()
            + "\n\n"
            + Bold(f"📤 Link Karma 🔮: {self.link_karma}").as_html()
            + "\n\n"
            + Bold(f"✅ Accept Chats 💭: {self.accept_chats}").as_html()
            + "\n\n"
            + Bold(f"✅ Accept PMs ✍️: {self.accept_pms}").as_html()
            + "\n\n"
            + Bold(f"✅ Accept Followers 🤝: {self.accept_followers}").as_html()
            + "\n\n"
            + Bold(f"✅ Verified 🔰: {self.verified}").as_html()
            + "\n\n"
            + Bold(f"⏳ Created UTC ⏳: {str(self.created_utc)}").as_html()
            + "\n\n"
        )


@dataclass
class Post:
    link: str
    id: str
    title: str
    author: str
    post_type: str  # Hot, New, Best, Top, Rising, etc.
    subreddit_name: str
    subreddit_id: str
    subreddit_tag: str
    subreddit_subscribers: int
    score: int
    comments_num: int
    upvote_ratio: float
    is_video: bool
    media_only: bool
    over_18: bool
    has_spoiler: bool
    created_at: datetime

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
        over_18 = (
            ""
            if self.over_18 is False
            else Bold(f"🔞 Over 18 🔞: {self.over_18}\n\n").as_html()
        )
        has_spoiler = (
            ""
            if self.has_spoiler is False
            else Bold(f"🌫With spoiler🌫: {self.has_spoiler}\n\n").as_html()
        )
        return (
            Bold(f"{self.post_type}🔥 from {self.subreddit.name}\n\n").as_html()
            + Bold("🔍 Title 🔍: ").as_html()
            + TextLink(self.title, url=self.link).as_html()
            + "\n\n"
            + Bold(f"✍️ Author ✍️: {self.author}\n\n").as_html()
            + Bold(f"💬 Comments Num 💬: {self.comments_num}\n\n").as_html()
            + Bold(f"⭐️ Score ⭐️: {self.score}\n\n").as_html()
            + Bold(f"👍 Upvote Ratio 👎: {self.upvote_ratio}\n\n").as_html()
            + Bold(f"📱 Media Only 📱: {self.media_only}\n\n").as_html()
            + Bold(f"🎥 Video 🎥: {self.is_video}\n\n").as_html()
            + over_18
            + has_spoiler
            + Bold(
                "⏳ Created UTC ⏳: {created_at} ({time_ago})\n\n".format(
                    created_at=str(self.created_at),
                    time_ago=self.__convert_time(datetime.utcnow() - self.created_at),
                )
            ).as_html()
            + HashTag(self.subreddit.tag).as_html()
            + ", "
            + HashTag("#" + self.subreddit.id).as_html()
        )


class RedditAPIException(Exception):
    pass
