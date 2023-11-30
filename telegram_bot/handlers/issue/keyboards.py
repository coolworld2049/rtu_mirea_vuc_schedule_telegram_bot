from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def issue_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Сообщить об ошибке",
            url="https://github.com/coolworld2049/rtu_mirea_vuc_schedule_telegram_bot/issues/new",
        ),
    )
    builder.adjust(2, 2)
    return builder
