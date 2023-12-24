from aiogram.types import Message
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from keyboards.reply_keyboards import main_kb, cancel_kb

router = Router()


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(text="Данной команды не существует ❌", reply_markup=main_kb)

@router.message(~StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(text="<b>Вы находитесь в заполнении формы</b>\n\nЧтобы отменить заполнение формы можно использовать команду <i>Отмена ❌</i> или введите <i>/cancel</i>", reply_markup=cancel_kb)
