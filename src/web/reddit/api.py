from datetime import datetime
from typing import Any, Optional, Union

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError

from .core import (
    LinkType,
    Post,
    PostType,
    RedditAPIException,
    Redditor,
    Result,
    SearchType,
    Sort,
    SubReddit,
    Time,
)


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
        return sort_redditors

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
                    language=subreddit["lang"],
                    id=subreddit["id"],
                    type=subreddit["subreddit_type"],
                    over_18=subreddit["over18"],
                    created_utc=datetime.fromtimestamp(subreddit["created_utc"]),
                )
            )
        return sort_subreddits

    def __tool_get_posts(
        self, user_posts: list[dict[str, Any]], **kwargs
    ) -> list[Post]:
        posts = []
        post_type: Optional[PostType] = kwargs.get("post_type")
        for post in user_posts:
            subreddit: str = kwargs.get("subreddit") if not None else post["subreddit"]
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
                    created_utc=datetime.fromtimestamp(post["created_utc"]),
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

    async def __tool_get_deviation(
        self,
        link_type: LinkType,
        session: ClientSession,
        **kwargs,
    ) -> int:
        if link_type == LinkType.GET_POSTS:
            subreddit = kwargs.get("subreddit")
            if not isinstance(subreddit, str):
                raise RedditAPIException("Kwarg subreddit doesn`t implement str type")
            post_type = kwargs.get("post_type")
            if not isinstance(post_type, PostType):
                raise RedditAPIException("Kwarg post_type doesn`t implement PostType")
            kwargs = {"subreddit": subreddit, "post_type": post_type.value}
        elif link_type == LinkType.SEARCH:
            request = kwargs.get("request")
            search_type = kwargs.get("search_type")
            sort_type = kwargs.get("sort_type")
            time = kwargs.get("time")
            if not isinstance(request, str):
                raise RedditAPIException("Kwarg request doesn`t implement str type")
            if not isinstance(search_type, SearchType):
                raise RedditAPIException(
                    "Kwarg search_type doesn`t implement SearchType"
                )
            elif search_type == SearchType.POST:
                if not isinstance(sort_type, Sort):
                    raise RedditAPIException("Kwarg sort_type doesn`t implement Sort")
                if not isinstance(time, Time):
                    raise RedditAPIException("Kwarg time doesn`t implement Time")
            kwargs = {
                "request": request,
                "type": search_type.value,
                "time": time.value,
                "sort": sort_type.value,
            }
        else:
            raise RedditAPIException("Arg link_type doesn`t implement LinkType")
        if not isinstance(session, ClientSession):
            raise RedditAPIException(
                "Arg session doesn`t implement aiohttp.ClientSession"
            )
        async with session.get(link_type.value.format(**kwargs, limit=150)) as resp:
            json: dict = await resp.json()
            if json.get("error") is None:
                deviation: int = json["data"]["dist"] - 100
            else:
                raise RedditAPIException("Request to reddit.com return error ...")
        return deviation

    async def check_subreddit(self, subreddit: str, session: ClientSession) -> bool:
        async with session.get(
            f"https://www.reddit.com/r/{subreddit}.json?", allow_redirects=False
        ) as res:
            try:
                json: dict = await res.json()
                if json.get("error") is None:
                    return True
                else:
                    return False
            except ContentTypeError:
                return False

    async def get_posts(
        self, subreddit: str, post_type: PostType = PostType.NEW, **kwargs
    ) -> Union[Result[Optional[list[Post]]]]:
        if not isinstance(post_type, PostType):
            raise RedditAPIException("Wrong param post_type")
        limit = kwargs.get("limit")
        async with ClientSession() as ses:
            if kwargs.get("is_check_subreddit"):
                if not await self.check_subreddit(subreddit, ses):
                    raise RedditAPIException("There is no such subreddit")
            deviation = await self.__tool_get_deviation(
                link_type=LinkType.GET_POSTS,
                session=ses,
                subreddit=subreddit,
                post_type=post_type,
            )
            limit_change = False
            if limit is None:
                pass
            elif deviation >= 0:
                limit = limit - deviation
            else:
                limit = 100 + deviation
                limit_change = True
            async with ses.get(
                "{link}r/{subreddit}/{post_type}.json?&limit={limit}".format(
                    link="https://www.reddit.com/",
                    subreddit=subreddit,
                    post_type=post_type.value,
                    limit=limit,
                )
            ) as res:
                json = await res.json()
                if json.get("error") is None:
                    reddit_posts = [post["data"] for post in json["data"]["children"]]
                    post_id = kwargs.get("post_id")
                    if not post_id:
                        return Result[list[Post]](
                            data=self.__tool_get_posts(
                                user_posts=reddit_posts,
                                subreddit=subreddit,
                                post_type=post_type,
                            ),
                            kwargs=dict(limit_change=limit_change),
                        )
                    else:
                        for post in reddit_posts:
                            if post["id"] == post_id:
                                index = reddit_posts.index(post)
                        return Result[list[Post]](
                            data=self.__tool_get_posts(
                                user_posts=reddit_posts[:index],
                                subreddit=subreddit,
                                post_type=post_type,
                            ),
                            kwargs=dict(limit_change=limit_change),
                        )
                else:
                    return Result[None].init(None)

    async def search_request(
        self, request: str, search_type: SearchType = SearchType.POST, **kwargs
    ) -> Result[Optional[list[Union[Post, Union[SubReddit, Redditor]]]]]:
        if not isinstance(search_type, SearchType):
            raise RedditAPIException("Wrong search_type param")
        limit = kwargs.get("limit")
        sort_type = kwargs.get("sort_type")
        time = kwargs.get("time")
        if search_type == SearchType.POST and (
            not isinstance(sort_type, Sort) and not isinstance(time, Time)
        ):
            raise RedditAPIException("Wrong sort_type for search_type 'link'")
        async with ClientSession() as ses:
            deviation = await self.__tool_get_deviation(
                link_type=LinkType.SEARCH,
                session=ses,
                request=request,
                search_type=search_type,
                sort_type=sort_type,
                time=time,
            )
            limit_change = False
            if limit is None:
                pass
            elif deviation >= 0:
                limit = limit - deviation
            else:
                limit = 100 + deviation
                limit_change = True
            async with ses.get(
                "{link}q={request}&limit={limit}&type={type}&sort={sort}&t={time}".format(
                    link="https://www.reddit.com/search/.json?",
                    request=request,
                    limit=limit,
                    type=search_type.value,
                    sort=sort_type.value,
                    time=time.value,
                )
            ) as res:
                json = await res.json()
                if json.get("error") is None:
                    data = [post["data"] for post in json["data"]["children"]]
                    if search_type == SearchType.POST:
                        return Result[list[Post]](
                            data=self.__tool_get_posts(
                                user_posts=data,
                                post_type=sort_type,
                            ),
                            kwargs=dict(limit_change=limit_change),
                        )
                    elif search_type == SearchType.SUBREDDIT:
                        return Result[list[SubReddit]](
                            data=self.__tool_get_subreddits(user_subreddits=data),
                            kwargs=dict(limit_change=limit_change),
                        )
                    else:
                        return Result[list[Redditor]](
                            data=self.__tool_get_redditors(user_redditors=data),
                            kwargs=dict(limit_change=limit_change),
                        )

                else:
                    return Result[None](None)

    def __str__(self) -> str:  # for tests
        return "Reddit API Object"
