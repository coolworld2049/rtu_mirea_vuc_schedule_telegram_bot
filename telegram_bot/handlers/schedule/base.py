from contextlib import suppress

from aiogram.types import CallbackQuery, Message
from rtu_mirea_vuc_schedule_client import (
    ApiClient,
    ScheduleApi,
    WeekScheduleResult,
    WorkbookApi,
)

from telegram_bot.handlers.utils import del_prev_message
from telegram_bot.schemas import UserSettingsBase
from telegram_bot.settings import settings
from telegram_bot.template_engine import render_template


async def common_schedule_logic(
    api_client,
    data: list[WeekScheduleResult],
    telegram_obj: Message | CallbackQuery,
    user_settings: UserSettingsBase,
):
    with suppress(Exception):
        await del_prev_message(telegram_obj)
        await telegram_obj.delete()
    bot = telegram_obj.bot
    relevance_date = await WorkbookApi(
        api_client,
    ).get_workbook_relevance_api_v1_workbook_relevance_get(
        course=user_settings.course,
    )
    text = ""
    for d in data:
        _text = render_template(
            "week_schedule.html",
            data=d,
            relevance_date=relevance_date.split("T")[0],
            user_settings=user_settings,
        )
        text += f"{_text}\n\n"
    return text


async def get_study_day_schedule(
    telegram_obj: Message | CallbackQuery, user_settings: UserSettingsBase, **kwargs
):
    async with ApiClient(settings.schedule_api_configuration) as api_client:
        data: list[WeekScheduleResult] = await ScheduleApi(
            api_client,
        ).get_week_schedule_api_v1_schedule_week_get(
            **user_settings.model_dump(exclude_none=True), **kwargs
        )
        return await common_schedule_logic(
            api_client=api_client,
            data=data,
            telegram_obj=telegram_obj,
            user_settings=user_settings,
        )


async def get_session_schedule(
    telegram_obj: Message | CallbackQuery, user_settings: UserSettingsBase, **kwargs
):
    async with ApiClient(settings.schedule_api_configuration) as api_client:
        data = await ScheduleApi(api_client).get_schedule_api_v1_schedule_get(
            **user_settings.model_dump(exclude_none=True), **kwargs
        )
        data = list(filter(lambda c: len(c.model_dump().get("schedule")) > 0, data))
        map_data = list(map(lambda c: c.schedule, data))
        map_data: list[WeekScheduleResult] = [
            x[0] for x in list(map(lambda c: c.schedule, data))
        ]
        return await common_schedule_logic(
            api_client=api_client,
            data=map_data,
            telegram_obj=telegram_obj,
            user_settings=user_settings,
        )
