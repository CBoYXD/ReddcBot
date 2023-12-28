from .hacknews import HackerNewsPostClick
from .lobster import LobsterPostClick
from .lemmy import LemmyPostClick
from .mastodon import MastodonPostClick
from .yt import YoutubePostClick
from .reddit import RedditPostClick


class PostClick:
    reddit = RedditPostClick()
    lemmy = LemmyPostClick()
    mastodon = MastodonPostClick()
    youtube = YoutubePostClick()
    lobster = LobsterPostClick()
    hack_news = HackerNewsPostClick()
