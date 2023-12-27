from typing import Any, Optional

import aiohttp
from core import Post, RedditAPIException, SubReddit


class RedditAPI:
    def __util_get_posts(
        self,
        user_posts: list[dict[str, Any]],
        subreddit: str,
        link: str,
        post_type: str,
    ) -> list[Post]:
        posts = []
        for post in user_posts:
            posts.append(
                Post(
                    link=link,
                    id=post["id"],
                    title=post["title"],
                    author=post["author"],
                    post_type=post_type,
                    topic=None,
                    subreddit=SubReddit(
                        name=subreddit,
                        id=post["subreddit_id"],
                        subscribers=post["subreddit_subscribers"],
                        tag="#" + subreddit,
                        reddit_tag="#" + "r/" + subreddit,
                    ),
                    created_at=post["created_utc"],
                    upvote_ratio=post["upvote_ratio"],
                    comments_num=post["num_comments"],
                    score=post["score"],
                    is_video=post["is_video"],
                    media_only=post["media_only"],
                    over_18=post["over_18"],
                )
            )
        return posts

    async def get_posts(
        self,
        subreddit: str,
        limit: int = 9,
        post_type: str = "new",
        id: Optional[str] = None,
    ) -> list[Post]:
        if post_type not in ("new", "hot", "top", "rising"):
            raise RedditAPIException("Wrong param post_type")
        link = f"https://www.reddit.com/r/{subreddit}/{post_type}.json?"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(link) as res:
                json = await res.json()
                reddit_posts = [post["data"] for post in json["data"]["children"]]
                if not id:
                    return self.__util_get_posts(
                        user_posts=reddit_posts[: limit - 1],
                        subreddit=subreddit,
                        link=link,
                        post_type=post_type,
                    )
                else:
                    for post in reddit_posts:
                        if post["id"] == id:
                            index = reddit_posts.index(post)
                    return self.__util_get_posts(
                        user_posts=reddit_posts[:index],
                        subreddit=subreddit,
                        link=link,
                        post_type=post_type,
                    )

    async def get_subreddits_posts(
        self,
        subreddits: tuple[
            tuple[str, Optional[str]]
        ],  # tuple((name, id), (name, id) ...)
        limit: int = 9,
        post_type: str = "new",
    ) -> list[Post]:
        if not isinstance(subreddits, tuple):
            raise RedditAPIException("Param 'subreddits' must be a tuple!")
        return [
            await self.get_posts(subreddit[0], limit, post_type, subreddit[1])
            for subreddit in subreddits
        ]

    async def check_subreddit(self, subreddit: str) -> bool:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://www.reddit.com/r/{subreddit}.json?") as res:
                json: dict = await res.json()
                if json.get("error") is None:
                    return True
                else:
                    return False

    async def check_subreddits(self, subreddits: list | tuple) -> tuple[str, bool]:
        return [
            (subreddit, await self.check_subreddit(subreddit))
            for subreddit in subreddits
        ]
