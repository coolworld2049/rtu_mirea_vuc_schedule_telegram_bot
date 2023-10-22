from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from telegram_bot.settings import settings

engine = create_async_engine(
    settings.async_db_url,
    echo=settings.db_echo,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    future=True,
)

async_session = async_sessionmaker(
    engine,
)
