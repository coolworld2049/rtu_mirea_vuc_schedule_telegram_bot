from aiogram import Router

from telegram_bot.handlers.schedule import schedule, current_week, next_week

router = Router(name=__file__)
router.include_routers(schedule.router, current_week.router, next_week.router)
