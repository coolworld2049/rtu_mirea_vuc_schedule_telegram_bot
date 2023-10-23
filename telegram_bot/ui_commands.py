from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_ui_commands(bot: Bot):
    await bot.set_my_description()
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    commands = [
        BotCommand(command="current_week", description="Учебный день текущей недели"),
        BotCommand(command="next_week", description="Учебный день следующей недели"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="schedule", description="Расписание по неделям"),
        BotCommand(command="platoons", description="Взводы Вашего курса"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
