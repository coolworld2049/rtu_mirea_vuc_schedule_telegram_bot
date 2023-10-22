from contextlib import suppress

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot import schemas
from telegram_bot.callbacks import UserSettingCallback
from telegram_bot.db import models
from telegram_bot.handlers.user_settings.keyboards import settings_keyboard
from telegram_bot.handlers.utils import del_prev_message, process_handler_error
from telegram_bot.states import UserSettingsState

router = Router(name=__file__)


async def user_settings_handler(bot: Bot, user: types.User, session: AsyncSession):
    user_obj = await session.execute(select(models.User).filter_by(id=user.id))
    db_user = user_obj.scalar()
    user_setting_obj = await session.execute(
        select(models.UserSettings).filter_by(user_id=user.id)
    )
    _user_setting = user_setting_obj.scalar()
    user_settings = (
        schemas.UserSettingsBase(**_user_setting.__dict__)
        if _user_setting
        else schemas.UserSettingsBase()
    )
    await bot.send_message(
        user.id,
        text="Для изменения нажмите на кнопку и введите новое значение",
        reply_markup=settings_keyboard(user_settings).as_markup(),
    )


@router.message(Command("settings"))
async def user_settings(message: types.Message, session: AsyncSession):
    with suppress(Exception):
        await del_prev_message(message)
        await message.delete()
    await user_settings_handler(message.bot, message.from_user, session)


@router.callback_query(
    UserSettingCallback.filter(F.name == "user-settings" and F.action == "set")
)
async def user_settings_callback(
    query: types.CallbackQuery,
    callback_data: UserSettingCallback,
    session: AsyncSession,
    state: FSMContext,
):
    await state.clear()
    await query.answer(f"Введите новый номер {callback_data.alter_key}")
    await state.update_data(callback_data=callback_data.model_dump(exclude_none=True))
    await state.set_state(UserSettingsState.set)


@router.message(UserSettingsState.set)
@process_handler_error
async def user_settings_set(
    message: types.Message, session: AsyncSession, state: FSMContext
):
    try:
        state_data = await state.get_data()
        if not state_data:
            return None
        callback_data: UserSettingCallback = UserSettingCallback(
            **state_data.get("callback_data")
        )
        await del_prev_message(message)
        values = schemas.UserSettingsBase(**{callback_data.key: message.text})
        allowed_courses = [str(x) for x in range(3, 6)]
        if values.course:
            assert int(values.course)
            if str(values.course) not in allowed_courses:
                raise ValueError(
                    f"Доступные номера курсов: {', '.join(allowed_courses)}"
                )
        if values.platoon:
            assert int(values.platoon)
        await session.execute(
            update(models.UserSettings)
            .where(models.UserSettings.user_id == message.from_user.id)
            .values(**values.model_dump(exclude_none=True))
        )
        await session.commit()
    except Exception as e:
        raise e
    finally:
        await state.clear()
        await user_settings_handler(message.bot, message.from_user, session)
