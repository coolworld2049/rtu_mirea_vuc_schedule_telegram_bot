from datetime import timedelta

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from telegram_bot.db.session import async_session
from telegram_bot.handlers import help, platoon, schedule, user_settings
from telegram_bot.loader import redis
from telegram_bot.middlewares import DbSessionMiddleware
from telegram_bot.middlewares.posthog import PosthogMiddleware
from telegram_bot.settings import settings

dp = Dispatcher(
    storage=RedisStorage(redis, state_ttl=timedelta(minutes=10)),
    name=__file__,
)

dp.update.middleware(DbSessionMiddleware(session_pool=async_session))
dp.update.middleware(PosthogMiddleware()) if settings.posthog_project_api_key else None
dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.include_routers(schedule.router, user_settings.router, platoon.router, help.router)
