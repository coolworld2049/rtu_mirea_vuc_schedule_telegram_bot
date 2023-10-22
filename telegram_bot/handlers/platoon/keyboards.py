import rtu_mirea_vuc_schedule_client
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.callbacks import PlatoonCallback


def platoon_keyboard(platoons: list[rtu_mirea_vuc_schedule_client.Platoon]):
    builder = InlineKeyboardBuilder()
    for platoon in platoons:
        builder.add(
            InlineKeyboardButton(
                text=f"{platoon.platoon_number} ({platoon.specialty_code})",
                callback_data=PlatoonCallback(
                    name="get",
                    platoon=platoon.platoon_number,
                ).pack(),
            )
        )
    builder.adjust(2, 2)
    return builder
