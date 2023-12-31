from .hacknews import HackerNewsPostClick
from .lemmy import LemmyPostClick
from .lobster import LobsterPostClick
from .mastodon import MastodonPostClick
from .reddit import RedditPostClick
from .yt import YoutubePostClick


class PostClick:
    reddit = RedditPostClick()
    lemmy = LemmyPostClick()
    mastodon = MastodonPostClick()
    youtube = YoutubePostClick()
    lobster = LobsterPostClick()
    hack_news = HackerNewsPostClick()
