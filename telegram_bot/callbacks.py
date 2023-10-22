from typing import Any

from aiogram.filters.callback_data import CallbackData


class UserSettingCallback(CallbackData, prefix="settings"):
    name: str
    key: str
    alter_key: str
    action: str = "change"


class ScheduleCallback(CallbackData, prefix="schedule"):
    name: str
    week_number: int
    date_str: Any = None


class PlatoonCallback(CallbackData, prefix="platoon"):
    name: str
    platoon: int
