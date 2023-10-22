from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot import schemas
from telegram_bot.db import models


async def create_user_with_settings(
    telegram_obj: types.Message | types.CallbackQuery, session: AsyncSession
):
    user_obj = schemas.User(
        id=telegram_obj.from_user.id,
        username=telegram_obj.from_user.username,
        full_name=telegram_obj.from_user.full_name,
    )
    user_setting_obj = schemas.UserSettings(
        user_id=telegram_obj.from_user.id,
    )
    try:
        session.add(
            models.User(**user_obj.model_dump(exclude_none=True)),
            _warn=False,
        )
    except:
        pass
    try:
        session.add(
            models.UserSettings(
                **user_setting_obj.model_dump(exclude_none=True),
            ),
            _warn=False,
        )
        await session.commit()
    except:
        await session.rollback()


async def get_user_settings(
    telegram_obj: types.Message | types.CallbackQuery, session: AsyncSession
):
    await create_user_with_settings(telegram_obj, session)
    user_setting_obj = await session.execute(
        select(models.UserSettings).filter_by(user_id=telegram_obj.from_user.id)
    )
    user_setting_obj = user_setting_obj.scalar()
    error_msg = "Установите номер курса и взвода /settings"
    if not user_setting_obj:
        raise ValueError(error_msg)
    user_setting = schemas.UserSettingsBase(**user_setting_obj.__dict__)
    if not user_setting.course or not user_setting.platoon:
        raise ValueError(error_msg)
    return user_setting
