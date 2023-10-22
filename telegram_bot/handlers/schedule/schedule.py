from contextlib import suppress

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.callbacks import ScheduleCallback
from telegram_bot.handlers.user_settings.base import get_user_settings
from telegram_bot.handlers.schedule.base import get_study_day_schedule
from telegram_bot.handlers.schedule.keyboards import scheduler_keyboard
from telegram_bot.handlers.utils import (
    del_prev_message,
    get_current_week,
    process_handler_error,
)

router = Router(name=__file__)


@router.message(Command("schedule"))
@process_handler_error
async def schedule(message: types.Message, session: AsyncSession):
    with suppress(Exception):
        await del_prev_message(message)
        await message.delete()
    current_week = await get_current_week()
    user_settings = await get_user_settings(message, session)
    markup = await scheduler_keyboard(current_week, user_settings=user_settings)
    await message.answer(
        f"Сейчас идет {current_week} неделя",
        reply_markup=markup.as_markup(),
    )


@router.callback_query(ScheduleCallback.filter(F.name == "get"))
@process_handler_error
async def schedule_callback(
    query: types.CallbackQuery, callback_data: ScheduleCallback, session: AsyncSession
):
    user_settings = await get_user_settings(query, session)
    data = await get_study_day_schedule(
        query,
        user_settings=user_settings,
        week=callback_data.week_number,
    )
    if not data:
        return
    await query.bot.send_message(query.from_user.id, text=data)
    with suppress(TelegramBadRequest):
        await query.message.delete()
