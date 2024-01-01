import aiohttp
import pytest

from src.web.reddit.api import RedditAPI
from src.web.reddit.core import Post, PostType


class TestRedditAPI:
    api = RedditAPI()
    request = "Ukraine"
    limit = 5
    post_type = PostType.HOT
    fake_subreddits = ("ggg", "soooo", "kkkkkkk", "soooooo")
    subreddits = ("AskReddit", "archlinux", "cpp")
    subreddits_id = ("t5_2qh1i", "t5_2qrzu", "t5_2qi27")  # (AskReddit, archlinux, cpp)

    @pytest.mark.asyncio
    async def test_get_subreddit_post(self):
        data = await self.api.get_posts(
            self.subreddits[0], self.post_type, limit=self.limit
        )
        data = data.data
        assert len(data) == self.limit
        for post in data:
            assert post.post_type.value == self.post_type.value
            assert post.subreddit_name == self.subreddits[0]
            assert post.subreddit_id == self.subreddits_id[0]
            assert post.subreddit_tag == f"#{self.subreddits[0]}"

    @pytest.mark.asyncio
    async def test_get_subreddits_posts(self):
        data = []
        for subreddit in self.subreddits:
            res = await self.api.get_posts(
                subreddit=subreddit, post_type=self.post_type, limit=self.limit
            )
            data.append(res.data)
        assert isinstance(data, list)
        assert len(data) == len(self.subreddits)
        for subreddit in enumerate(data):
            assert isinstance(subreddit[1], list)
            assert len(subreddit[1]) == self.limit
            for post in enumerate(subreddit[1]):
                assert isinstance(post[1], Post)
                assert post[1].post_type.value == self.post_type.value
                subreddit_name = self.subreddits[subreddit[0]]
                assert post[1].subreddit_name == subreddit_name
                assert post[1].subreddit_id == self.subreddits_id[subreddit[0]]
                assert post[1].subreddit_tag == f"#{subreddit_name}"

    @pytest.mark.asyncio
    async def test_check_subreddits(self):
        async with aiohttp.ClientSession() as session:
            for subreddit in self.fake_subreddits:
                await self.api.check_subreddit(subreddit, session) is False
            for subreddit in self.subreddits:
                await self.api.check_subreddit(subreddit, session) is True
