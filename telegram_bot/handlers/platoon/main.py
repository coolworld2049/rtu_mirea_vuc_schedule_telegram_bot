import json

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from rtu_mirea_vuc_schedule_client import ApiException, ApiClient, ScheduleApi
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot.handlers.user_settings.base import get_user_settings
from telegram_bot.handlers.platoon.keyboards import platoon_keyboard
from telegram_bot.handlers.utils import del_prev_message, process_handler_error
from telegram_bot.settings import settings

router = Router(name=__file__)


@router.message(Command("platoons"))
@process_handler_error
async def platoons(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await del_prev_message(message)
    user_setting = await get_user_settings(message, session)
    text = f"{user_setting.course} курс"
    async with ApiClient(settings.schedule_api_configuration) as api_client:
        try:
            data = await ScheduleApi(
                api_client
            ).get_platoons_api_v1_schedule_platoons_get(course=user_setting.course)
            await message.answer(
                text=text,
                reply_markup=platoon_keyboard(data).as_markup(),
            )
        except ApiException as ae:
            await message.answer(text=json.loads(ae.body).get("detail"))
