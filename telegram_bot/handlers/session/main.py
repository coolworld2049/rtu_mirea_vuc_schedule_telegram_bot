from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.handlers.schedule.base import get_session_schedule
from telegram_bot.handlers.user_settings.base import get_user_settings
from telegram_bot.handlers.utils import del_prev_message

router = Router(name=__file__)


@router.message(Command("session"))
async def session_schedule(message: types.Message, session: AsyncSession):
    await del_prev_message(message)

    user_settings = await get_user_settings(message, session)
    text = await get_session_schedule(
        message,
        user_settings=user_settings,
        where="зачет",
    )
    exams_text = await get_session_schedule(
        message,
        user_settings=user_settings,
        where="экзамен",
    )
    text = f"<em>Зачеты</em>\n\n{text}\n\n<em>Экзамены</em>\n\n{exams_text}"
    if not text:
        return
    await message.answer(text=text)
