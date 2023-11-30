from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from loguru import logger


async def set_ui_commands(bot: Bot):
    try:
        await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
        commands = [
            BotCommand(
                command="current_week",
                description="Учебный день текущей недели",
            ),
            BotCommand(
                command="next_week",
                description="Учебный день следующей недели",
            ),
            BotCommand(command="settings", description="Настройки"),
            BotCommand(command="schedule", description="Расписание по неделям"),
            BotCommand(command="session", description="Зачеты и экзамены"),
            BotCommand(command="platoons", description="Взводы Вашего курса"),
            BotCommand(command="issue", description="Сообщить об ошибке"),
        ]
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats(),
        )
    except Exception as e:
        logger.error(e)
