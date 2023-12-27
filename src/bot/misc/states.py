from aiogram.fsm.state import State, StatesGroup


class AdminStatePosts(StatesGroup):
    choose = State()


class AdminState(StatesGroup):
    posts = AdminStatePosts()
