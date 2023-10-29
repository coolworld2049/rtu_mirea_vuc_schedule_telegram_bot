import asyncio
import json
from contextlib import suppress
from functools import wraps

import aiohttp
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiohttp import ClientConnectorError
from loguru import logger
from pydantic_core import ValidationError
from rtu_mirea_vuc_schedule_client import ApiException


def process_handler_error(func):
    async def process_error(e: str, *args, **kwargs):
        logger.error(e)
        telegram_obj: types.Message | types.CallbackQuery = args[0]
        sleep_time_sec = 2 + round(len(e) / 50, 1)
        text = (
            f"Ошибка:\n\n"
            f"{e.strip()}"
            f"\n\nЭто сообщение будет <b>удалено</b> через <b>{int(sleep_time_sec)} секунды</b>❗"
        )
        telegram_obj_answer = await telegram_obj.answer(text)
        await asyncio.sleep(sleep_time_sec)
        await telegram_obj_answer.delete()
        with suppress(TelegramBadRequest):
            for m_id in range(
                telegram_obj_answer.message_id - 1,
                telegram_obj_answer.message_id + 1,
            ):
                await telegram_obj.bot.delete_message(telegram_obj.from_user.id, m_id)
        try:
            return await func(*args, **kwargs)
        except:
            pass

    @wraps(func)
    async def process_handler_error_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as ve:
            msg = [
                f" {', '.join(err['loc'])}: {err['msg']}"
                for err in ve.errors(
                    include_url=False,
                )
            ]
            await process_error("\n".join(msg), *args, **kwargs)
        except ApiException as ae:
            detail = json.loads(ae.body).get("detail")
            await process_error(detail, *args, **kwargs)
        except ClientConnectorError as ce:
            logger.error(ce)
            msg = "Сервис временно недоступен"
            await process_error(msg, *args, **kwargs)
        except ValueError as e:
            await process_error(str(e), *args, **kwargs)

    return process_handler_error_wrapper


async def del_prev_message(message):
    with suppress(TelegramBadRequest):
        await message.bot.delete_message(message.from_user.id, message.message_id - 1)


async def get_current_week():
    url = "https://timetable.mirea.ru/api/current-week"
    headers = {"accept": "application/json"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                if response.status == 200:
                    week: int = data["week"]
                    return week
                else:
                    logger.error(f"Request failed with status code {response.status}")
                return data
        except aiohttp.ClientError as e:
            logger.error(f"An error occurred during the request: {e}")
            raise e
