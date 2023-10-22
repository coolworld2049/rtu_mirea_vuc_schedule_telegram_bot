from aiogram import Bot
from redis.asyncio import Redis

from telegram_bot.settings import settings

redis = Redis.from_url(settings.redis_url.__str__())
bot = Bot(token=settings.token, parse_mode="html")
