import aiogram
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

bot = Bot(token='7371152325:AAFCtleaVO1iCbcoHcmyVBV1DiOnMelazDE')

dp = Dispatcher()
router = Router()


class Form(StatesGroup):
    waiting_for_name = State()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    start_message = open('messages/start_message.txt')
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="ЖАТАХАНА ҮШІН", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F"),
        InlineKeyboardButton(text="ТАМАҚТАНУ ҮШІН", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F"),
    )
    reply_markup=keyboard_builder.as_markup()
    await message.answer(start_message.read(), reply_markup=reply_markup)

    await message.answer('📃 Толық аты жөніңізді жазыңыз:')
    await state.set_state(Form.waiting_for_name)


@router.message(Form.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    # Get the user's name from their response
    user_name = message.text
    # Reply with a greeting message
    await message.answer(f"Nice to meet you, {user_name}!")
    # Clear the state
    await state.clear()


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())