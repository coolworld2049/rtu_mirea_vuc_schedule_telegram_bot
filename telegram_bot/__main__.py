import asyncio

from loguru import logger

from telegram_bot._logging import configure_logging
from telegram_bot.db.utils import wait_for_db, metadata_create_all
from telegram_bot.dispatcher import dp
from telegram_bot.loader import bot
from telegram_bot.settings import settings
from telegram_bot.ui_commands import set_ui_commands


async def main():
    if await wait_for_db():
        configure_logging(settings.log_level.upper())
        await metadata_create_all()
        await set_ui_commands(bot)
        await dp.start_polling(bot, polling_timeout=5)
        logger.info("Telegram bot started")


asyncio.run(main())
