from aiogram.fsm.state import State, StatesGroup


class AdminRedditStatePosts(StatesGroup):
    choose_subreddit = State()


class AdminStatePosts(StatesGroup):
    choose_network = State()
    reddit = AdminRedditStatePosts()


class AdminState(StatesGroup):
    posts = AdminStatePosts()
