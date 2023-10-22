from aiogram.fsm.state import StatesGroup, State


class UserSettingsState(StatesGroup):
    set = State()
