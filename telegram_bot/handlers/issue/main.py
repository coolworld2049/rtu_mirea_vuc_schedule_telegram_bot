from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.handlers.issue.keyboards import issue_keyboard
from telegram_bot.handlers.utils import del_prev_message

router = Router(name=__file__)


@router.message(Command("issue"))
async def help(message: types.Message, state: FSMContext):
    await state.clear()
    await del_prev_message(message)
    await message.answer(
        "Информация",
        reply_markup=issue_keyboard().as_markup(),
    )
