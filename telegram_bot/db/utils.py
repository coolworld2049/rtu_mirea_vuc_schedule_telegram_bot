import tenacity
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from telegram_bot.db.models import Base
from telegram_bot.db.session import engine
from telegram_bot.settings import settings


@tenacity.retry(
    retry=tenacity.retry_if_result(lambda result: not result),
    wait=tenacity.wait_fixed(2),
    stop=tenacity.stop_after_delay(300),
    reraise=True,
)
async def wait_for_db():
    try:
        async with engine.begin() as conn:
            conn: AsyncConnection
            await conn.execute(text("select 1"))
            return True
    except Exception as e:
        logger.error(f"{settings.db_host}:{settings.db_port} {e}")
        return False


async def metadata_create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
