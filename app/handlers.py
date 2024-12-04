import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as keyboards

router = Router()

# Создание состояний для анкеты
class Registration(StatesGroup):
    surname = State()
    name = State()
    gender = State()
    faculty = State()
    specialty = State()
    course = State()
    city = State()
    room = State()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=keyboards.main)

# Обработка нажатия на кнопку "Заполнить анкету"
@router.message(F.text == "Заполнить анкету 📝")
async def register(message: Message, state: FSMContext):
    await state.set_state(Registration.surname)
    await message.answer('Введите вашу фамилию:')

# Обработка фамилии
@router.message(Registration.surname)
async def register_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Registration.name)
    await message.answer('Введите ваше имя:')

# Обработка имени
@router.message(Registration.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.gender)
    await message.answer('Выберите ваш пол:', reply_markup=keyboards.gender_keyboard())

# Обработка выбора гендера
@router.callback_query(lambda c: c.data.startswith('gender_'))
async def process_gender(callback_query: CallbackQuery, state: FSMContext):
    gender = callback_query.data.split('_')[1]
    await state.update_data(gender=gender)
    await state.set_state(Registration.faculty)
    await callback_query.message.answer('Выберите ваш факультет:', reply_markup=await keyboards.faculty_keyboard())
    await callback_query.answer()

# Обработка выбора факультета
@router.callback_query(lambda c: c.data.startswith('faculty_'))
async def process_faculty(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Received callback data: {callback_query.data}")
    faculty = callback_query.data.split('_', 1)[1]
    await state.update_data(faculty=faculty)

    await state.set_state(Registration.specialty)

    specialty_keyboard = await keyboards.specialty_keyboard(faculty)
    await callback_query.message.answer(
        f'Выберите специальность для факультета {faculty}:',
        reply_markup=specialty_keyboard
    )

    await callback_query.answer()


# Обработка выбора специальности
@router.callback_query(lambda c: c.data.startswith('specialty_'))
async def process_specialty(callback_query: CallbackQuery, state: FSMContext):
    specialty = callback_query.data.split('_', 1)[1]
    await state.update_data(specialty=specialty)

    await state.set_state(Registration.room)

    await callback_query.message.answer('Выберите комнату:', reply_markup=await keyboards.room_keyboard())

    await callback_query.answer()

# Обработка нажатии на кнопку "Назад"
@router.callback_query(lambda c: c.data == 'back')
async def process_back(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.faculty)

    await callback_query.message.answer('Выберите ваш факультет:', reply_markup=await keyboards.faculty_keyboard())

    await callback_query.answer()

# Обработка города
@router.callback_query(lambda c: c.data.startswith('room_'))
async def register_course(callback_query: CallbackQuery, state: FSMContext):
    room = callback_query.data.split('_')[1]
    await state.update_data(room=room)
    await state.set_state(Registration.course)

    await callback_query.message.answer("Выберите курс: ")

    await callback_query.answer()

# Обработка города
@router.message(Registration.course)
async def register_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(Registration.city)
    await message.answer('Введите ваш город:')

# Завершение регистрации
@router.message(Registration.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    await message.answer(f'Регистрация завершена!\n'
                         f'Фамилия: {data["surname"]}\n'
                         f'Имя: {data["name"]}\n'
                         f'Пол: {data["gender"]}\n'
                         f'Факультет: {data["faculty"]}\n'
                         f'Специальность: {data["specialty"]}\n'
                         f'Курс: {data["course"]}\n'
                         f'Город: {data["city"]}\n'
                         f'Комната: {data.get("room", "Не выбрана")}\n')
    await state.clear()
