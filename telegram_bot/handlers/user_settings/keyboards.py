from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from telegram_bot.callbacks import UserSettingCallback
from telegram_bot.schemas import UserSettingsBase


def settings_keyboard(user_settings: UserSettingsBase):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=f"{user_settings.course or ''} курс",
            callback_data=UserSettingCallback(
                name="user-settings",
                key="course",
                alter_key="курса",
                action="set",
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f"{user_settings.platoon or ''} взвод",
            callback_data=UserSettingCallback(
                name="user-settings",
                key="platoon",
                alter_key="взвода",
                action="set",
            ).pack(),
        ),
    )
    builder.adjust(1, 1)
    return builder
