from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from cashews import cache
from rtu_mirea_vuc_schedule_client import ApiClient, ScheduleApi

from telegram_bot.callbacks import ScheduleCallback
from telegram_bot.schemas import UserSettings
from telegram_bot.settings import settings


@cache(ttl="12h", lock=True)
async def scheduler_keyboard(current_week: int, user_settings: UserSettings):
    builder = InlineKeyboardBuilder()
    async with ApiClient(settings.schedule_api_configuration) as api_client:
        data = await ScheduleApi(api_client).get_days_week_api_v1_schedule_daily_get(
            **user_settings.model_dump(exclude_none=True)
        )
    for w in data:
        day = w.days[0].day if len(w.days) > 0 else None
        if day:
            text = f"{w.week} неделя - {day}"
            if w.week == current_week:
                text = text.upper()
            builder.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=ScheduleCallback(
                        name="get",
                        week_number=w.week,
                        day_str=day,
                    ).pack(),
                ),
            )
    builder.adjust(1, 1)
    return builder
