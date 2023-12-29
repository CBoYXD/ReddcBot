from typing import Any, Optional

import aiohttp
from datetime import datetime
from .core import RedditAPIException, Post, SubReddit, Redditor


class RedditAPI:
    def __tool_get_redditors(
        self, user_redditors: list[dict[str, Any]]
    ) -> list[Redditor]:
        sort_redditors = []
        for redditor in user_redditors:
            name = redditor["name"]
            sort_redditors.append(
                Redditor(
                    name=name,
                    id=redditor["id"],
                    link=f"https://www.reddit.com/user/{name}",
                    comment_karma=redditor["comment_karma"],
                    link_karma=redditor["link_karma"],
                    created_utc=datetime.fromtimestamp(redditor["created_utc"]),
                    accept_chats=redditor["accept_chats"],
                    accept_pms=redditor["accept_pms"],
                    accept_followers=redditor["accept_followers"],
                    verified=redditor["verified"],
                )
            )

    def __tool_get_subreddits(
        self, user_subreddits: list[dict[str, Any]]
    ) -> list[SubReddit]:
        sort_subreddits = []
        for subreddit in user_subreddits:
            name = subreddit["display_name"]
            sort_subreddits.append(
                SubReddit(
                    name=name,
                    link=f"https://www.reddit.com/r/{name}",
                    title=subreddit["title"],
                    lang=subreddit["lang"],
                    id=subreddit["id"],
                    type=subreddit["subreddit_type"],
                    over_18=subreddit["over18"],
                    created_at=datetime.fromtimestamp(subreddit["created_utc"]),
                )
            )

    def __tool_get_posts(
        self,
        user_posts: list[dict[str, Any]],
        subreddit: Optional[str] = None,
        post_type: Optional[str] = None,
    ) -> list[Post]:
        subreddit = subreddit if not None else user_posts["subreddit"]
        posts = []
        for post in user_posts:
            posts.append(
                Post(
                    link=f"https://www.reddit.com{post['permalink']}",
                    id=post["id"],
                    title=post["title"],
                    author=post["author"],
                    post_type=post_type,
                    subreddit_name=subreddit,
                    subreddit_id=post["subreddit_id"],
                    subreddit_subscribers=post["subreddit_subscribers"],
                    subreddit_tag="#" + subreddit,
                    created_at=datetime.fromtimestamp(post["created_utc"]),
                    upvote_ratio=post["upvote_ratio"],
                    comments_num=post["num_comments"],
                    score=post["score"],
                    is_video=post["is_video"],
                    media_only=post["media_only"],
                    over_18=post["over_18"],
                    has_spoiler=post["spoiler"],
                )
            )
        return posts

    async def get_posts(
        self,
        subreddit: str,
        post_type: str = "new",
        limit: Optional[int] = None,
        id: Optional[str] = None,
    ) -> list[Post]:
        if post_type not in ("new", "hot", "top", "rising"):
            raise RedditAPIException("Wrong param post_type")
        if limit is not None and (0 > limit or limit > 100):
            raise RedditAPIException("Param limit can only be from 0 to 100 inclusive")
        if (limit is not None) and (id is not None):
            raise RedditAPIException(
                "Params limit and id cannot be true at the same time "
                + "(one of the parameters must be None)"
            )

        async with aiohttp.ClientSession() as ses:
            async with ses.get(
                "{link}r/{subreddit}/{post_type}.json?&{limit}".format(
                    link="https://www.reddit.com/",
                    subreddit=subreddit,
                    post_type=post_type,
                    limit=limit,
                )
            ) as res:
                json = await res.json()
                reddit_posts = [post["data"] for post in json["data"]["children"]]
                if not id:
                    return self.__tool_get_posts(
                        user_posts=reddit_posts,
                        subreddit=subreddit,
                        post_type=post_type,
                    )
                else:
                    for post in reddit_posts:
                        if post["id"] == id:
                            index = reddit_posts.index(post)
                    return self.__tool_get_posts(
                        user_posts=reddit_posts[:index],
                        subreddit=subreddit,
                        post_type=post_type,
                    )

    async def get_subreddits_posts(
        self,
        subreddits: tuple[
            tuple[str, Optional[str]]
        ],  # tuple((name, id), (name, id), ...)
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

    async def check_subreddits(
        self, subreddits: list | tuple
    ) -> list[tuple[str, bool]]:
        return [
            (subreddit, await self.check_subreddit(subreddit))
            for subreddit in subreddits
        ]

    async def search_request(
        self,
        request: str,
        search_type: str = "link",
        limit: Optional[int] = None,
        sort_type: Optional[str] = None,
        time: Optional[str] = None,
    ) -> list[Post] | None:
        if search_type not in ("link", "sr", "user"):
            raise RedditAPIException("Wrong search_type param")
        if limit is not None and (0 > limit or limit > 100):
            raise RedditAPIException("Param limit can only be from 0 to 100 inclusive")
        if search_type == "link" and (
            sort_type not in ("relevance", "hot", "new", "comments", "top")
        ):
            raise RedditAPIException("Wrong sort_type for search_type 'link'")
        elif search_type != "link" and (time or sort_type):
            raise RedditAPIException(
                "Params time and sort_type can be only None, "
                "if param search_type != link"
            )
        async with aiohttp.ClientSession() as ses:
            async with ses.get(
                "{link}q={request}&{limit}&{type}&{sort}&{time}".format(
                    link="https://www.reddit.com/search/.json?",
                    request=request,
                    limit=limit,
                    type=search_type,
                    sort=sort_type,
                    time=time,
                )
            ) as res:
                json = await res.json()
                if json.get("error") is None:
                    data = [post["data"] for post in json["data"]["children"]]
                    if search_type == "link":
                        return self.__tool_get_posts(
                            user_posts=data,
                            post_type=sort_type,
                        )
                    elif search_type == "sr":
                        return self.__tool_get_subreddits(user_subreddits=data)
                    else:
                        return self.__tool_get_redditors(user_redditors=data)

                else:
                    return None

    def __str__(self) -> str:  # for tests
        return "Reddit API Object"
