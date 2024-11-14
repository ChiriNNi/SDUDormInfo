import os
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from models import StudentInfo
from views import *
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=storage)
router = Router()


@router.message(F.text == "/start")
async def language_choice(message: Message, state: FSMContext):
    await message.answer("Тілді таңдаңыз/Выберите язык", reply_markup=language_button())

    await state.set_state(StudentInfo.language)


@dp.callback_query(lambda c: c.data in ['ru', 'kz'])
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    StudentInfo.language = callback.data
    await callback.message.answer(start(StudentInfo.language).read())
    await callback.message.answer("Толық аты-жөніңізді жазыңыз" if StudentInfo.language == "kz" else "Напишите полное имя")
    await state.set_state(StudentInfo.waiting_for_full_name)


@router.message(StudentInfo.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    user_name = message.text
    data = await state.get_data()
    lang = data.get("language")
    print(f"Student id: {message.chat.id} \n Student full_name: {user_name}\n {StudentInfo.language}")
    await message.answer("Қалаңызды жазыңыз" if StudentInfo.language == "kz" else "Напишите свой город")
    await state.set_state(StudentInfo.waiting_for_city)


@router.message(StudentInfo.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    print(f"Student id: {message.chat.id} \n Student city: {city}\n")

    await message.answer("Курсыңызды жазыңыз" if StudentInfo.language == "kz" else "Напишите свой курс")
    await state.set_state(StudentInfo.waiting_for_course)


@router.message(StudentInfo.waiting_for_course)
async def process_course(message: Message, state: FSMContext):
    course = message.text
    print(f"Student id: {message.chat.id} \n Student course: {course}\n")

    await message.answer("Мамандығыңызды жазыңыз" if StudentInfo.language == "kz" else "Напишите свою специальность")
    await state.set_state(StudentInfo.waiting_for_speciality)


@router.message(StudentInfo.waiting_for_speciality)
async def process_speciality(message: Message, state: FSMContext):
    speciality = message.text
    print(f"Student id: {message.chat.id} \n Student speciality: {speciality}\n")

    await message.answer("Жыныс" if StudentInfo.language == "kz" else "Выберите пол", reply_markup=gender_button())
    await state.set_state(StudentInfo.waiting_for_gender)

    await state.clear()


@router.message(StudentInfo.waiting_for_room)
@dp.callback_query(lambda c: c.data in ["Мужчина", "Женщина"])
async def handle_gender(callback: CallbackQuery, state: FSMContext):
    print(f"Student id: {callback.message.chat.id} \n Student gender: {callback.data}\n")

    await bot.send_message(callback.message.chat.id,"Бөлме таңдаңыз" if StudentInfo.language == "kz" else "Выберите комнату", reply_markup=rooms())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    await state.set_state(StudentInfo.waiting_for_room)
    await state.clear()


@dp.callback_query(F.data == 'room')
async def handle_room(callback: CallbackQuery):
    room = callback.message
    print(room)


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
