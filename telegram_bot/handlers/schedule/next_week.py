from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.handlers.schedule.base import get_study_day_schedule
from telegram_bot.handlers.user_settings.base import get_user_settings
from telegram_bot.handlers.utils import (
    del_prev_message,
    get_current_week,
    process_handler_error,
)

router = Router(name=__file__)


@router.message(Command("next_week"))
@process_handler_error
async def current_week(message: types.Message, session: AsyncSession):
    await del_prev_message(message)

    user_settings = await get_user_settings(message, session)
    week_number = await get_current_week()
    text = await get_study_day_schedule(
        message, user_settings=user_settings, week=week_number + 1
    )
    if not text:
        return
    await message.answer(text=text)
