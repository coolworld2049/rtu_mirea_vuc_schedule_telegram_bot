from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.handlers.help.keyboards import help_keyboard
from telegram_bot.handlers.utils import del_prev_message

router = Router(name=__file__)


@router.message(Command("help"))
async def help(message: types.Message, state: FSMContext):
    await state.clear()
    await del_prev_message(message)
    await message.answer(
        "Помощь",
        reply_markup=help_keyboard().as_markup(),
    )
