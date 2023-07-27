from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchState(StatesGroup):
    search = State()
