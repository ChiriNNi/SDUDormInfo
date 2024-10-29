import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from models import StudentInfo
from views import *


bot = Bot(token='7371152325:AAFCtleaVO1iCbcoHcmyVBV1DiOnMelazDE')
dp = Dispatcher()
router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(start().read(), reply_markup=payment_button())
    await message.answer('Напишите полное имя: ')
    await state.set_state(StudentInfo.waiting_for_full_name)


@router.message(StudentInfo.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    user_name = message.text
    print(f"Student id: {message.chat.id} \n Student full_name: {user_name}\n")
    await message.answer("Напишите свой город: ")
    await state.set_state(StudentInfo.waiting_for_city)


@router.message(StudentInfo.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    print(f"Student id: {message.chat.id} \n Student city: {city}\n")

    await message.answer("Напишите свой курс")
    await state.set_state(StudentInfo.waiting_for_course)


@router.message(StudentInfo.waiting_for_course)
async def process_course(message: Message, state: FSMContext):
    course = message.text
    print(f"Student id: {message.chat.id} \n Student course: {course}\n")

    await message.answer("Напишите свою специальность")
    await state.set_state(StudentInfo.waiting_for_speciality)


@router.message(StudentInfo.waiting_for_speciality)
async def process_speciality(message: Message, state: FSMContext):
    speciality = message.text
    print(f"Student id: {message.chat.id} \n Student speciality: {speciality}\n")

    await message.answer("Выберите пол", reply_markup=gender_button())
    await state.set_state(StudentInfo.waiting_for_gender)

    await state.clear()


@dp.callback_query(F.data == 'option_1')
async def handle_1(callback: CallbackQuery):
    choice = "Мужчина"
    print(f"Student id: {callback.message.chat.id} \n Student gender: {choice}\n")


@dp.callback_query(F.data == 'option_2')
async def handle_2(callback: CallbackQuery):
    choice = "Женщина"
    print(f"Student id: {callback.message.chat.id} \nStudent gender: {choice}")


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())