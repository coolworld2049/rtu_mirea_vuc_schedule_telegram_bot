from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    await bot.set_my_description()
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    commands = [
        BotCommand(command="next_week", description="Учебный день следующей недели"),
        BotCommand(command="current_week", description="Учебный день текущей недели"),
        BotCommand(command="schedule", description="Расписание по неделям"),
        BotCommand(command="platoons", description="Взводы Вашего курса"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
