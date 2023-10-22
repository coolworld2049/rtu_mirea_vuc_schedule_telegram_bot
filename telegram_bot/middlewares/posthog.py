from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject, CallbackQuery
from posthog import Posthog

from telegram_bot.settings import settings


class PosthogMiddleware(BaseMiddleware):
    def __init__(self, posthog_client: Posthog = None):
        super().__init__()
        self.posthog_client = posthog_client or Posthog(
            project_api_key=settings.posthog_project_api_key,
            host="https://app.posthog.com",
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        _event = event.event
        posthog_event = None
        if isinstance(_event, types.Message):
            posthog_event = _event.text
        elif isinstance(_event, CallbackQuery):
            posthog_event = _event.data
        self.posthog_client.capture(
            distinct_id=_event.from_user.username,
            event=posthog_event,
            timestamp=datetime.now(),
        )
        return await handler(event, data)
