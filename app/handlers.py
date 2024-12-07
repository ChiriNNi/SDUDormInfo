import asyncio
import logging
import os
from datetime import datetime

from app.approve import start_timer, update_payment_status
from config import TOKEN
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ContentType
import app.keyboards as keyboards
from app.database.requests import post_user, get_roommates, get_faculty, get_specialty_one

#from app.database.requests import post_user

router = Router()
bot = Bot(token=TOKEN)

# Создание состояний для анкеты
class Registration(StatesGroup):
    surname = State()
    name = State()
    gender = State()
    faculty = State()
    specialty = State()
    phone_number = State()
    city = State()
    room = State()
    sleep_mode = State()
    wake_up_time = State()
    noise_at_night = State()
    order_room = State()
    religion = State()
    roommate_traits = State()
    wishes = State()
    payment_accommodation = State()
    payment_food = State()
    is_approved_payment = State()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=keyboards.main)

@router.message(F.text == "Информация о общежитии 🏠")
async def register(message: Message, state: FSMContext):
    information_message = open("messages/main_information.txt", "r")
    await state.set_state(Registration.surname)
    await message.answer(information_message.read(), reply_markup=keyboards.main)

# Обработка нажатия на кнопку "Заполнить анкету"
@router.message(F.text == "Заполнить анкету 📝")
async def register(message: Message, state: FSMContext):
    await state.set_state(Registration.surname)
    await message.answer('Введите вашу фамилию:', reply_markup=ReplyKeyboardRemove())

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
    ru_gender = {
        "male": "Мужской",
        "female": "Женский"
    }
    await callback_query.message.edit_text(f"Ваш пол: {ru_gender[gender]}")
    await state.update_data(gender=gender)
    await state.set_state(Registration.faculty)
    await callback_query.message.answer('Выберите ваш факультет:', reply_markup= await keyboards.faculty_keyboard())
    await callback_query.answer()

# Обработка выбора факультета
@router.callback_query(lambda c: c.data.startswith('faculty_'))
async def process_faculty(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f"Received callback data: {callback_query.data}")
    faculty = callback_query.data.split('_', 1)[1]
    await state.update_data(faculty=faculty)
    await state.set_state(Registration.specialty)

    await callback_query.message.delete()

    specialty_keyboard = await keyboards.specialty_keyboard(faculty)
    await callback_query.message.answer(
        f'Выберите специальность для факультета {faculty}:',
        reply_markup=specialty_keyboard
    )

    await callback_query.answer()


# Обработка выбора специальности
@router.callback_query(lambda c: c.data.startswith('specialty_'))
async def process_specialty(callback_query: CallbackQuery, state: FSMContext):
    specialty = callback_query.data.split('_')[1]

    await state.update_data(specialty=specialty)
    await callback_query.message.delete()
    await callback_query.message.answer("Сейчас вы должны ответить на некоторые вопросы (честно). \n\nВАШИ ОТВЕТЫ БУДУТ ВИДНЫ ДРУГИМ ПОЛЬЗОВАТЕЛЯМ")

    # await state.set_state(Registration.room)
    await state.set_state(Registration.sleep_mode)
    await callback_query.message.answer("Во сколько вы обычно ложитесь спать?", reply_markup= keyboards.sleep_keyboard())

@router.callback_query(lambda c: c.data.startswith('sleep_'))
async def process_sleep_mode(callback_query: CallbackQuery, state: FSMContext):
    sleep_mode = callback_query.data.split('_')[1]
    await callback_query.message.delete()
    await state.update_data(sleep_mode=sleep_mode)

    await state.set_state(Registration.wake_up_time)
    await callback_query.message.answer("Во сколько вы обычно просыпаетесь?", reply_markup= keyboards.wake_keyboard())

@router.callback_query(lambda c: c.data.startswith('wake_'))
async def process_wake_up(callback: CallbackQuery, state: FSMContext):
    wake_up_time = callback.data.split("_")[1]
    await callback.message.delete()
    await state.update_data(wake_up_time=wake_up_time)

    await state.set_state(Registration.noise_at_night)
    await callback.message.answer("Как вы относитесь к шуму в комнате вечером?", reply_markup= keyboards.noise_keyboard())

@router.callback_query(lambda c: c.data.startswith('silence_'))
async def process_noise_at_night(callback: CallbackQuery, state: FSMContext):
    noise_at_night = callback.data.split("_")[1]
    await callback.message.delete()
    await state.update_data(noise_at_night=noise_at_night)
    await state.set_state(Registration.order_room)
    await callback.message.answer("Как вы относитесь к порядку в общей части комнаты?", reply_markup= keyboards.order_keyboard())

@router.callback_query(lambda c: c.data.startswith('order_'))
async def process_order_room(callback: CallbackQuery, state: FSMContext):
    order_room = callback.data.split("_")[1]
    await callback.message.delete()
    await state.update_data(order_room=order_room)
    await state.set_state(Registration.religion)
    await callback.message.answer("Насколько важно, чтобы ваш руммейт был религиозным?", reply_markup= keyboards.religion_keyboard())

@router.callback_query(lambda c: c.data.startswith('religion_'))
async def process_religion(callback: CallbackQuery, state: FSMContext):
    religion = callback.data.split("_")[1]
    await callback.message.delete()
    await state.update_data(religion=religion)
    await state.set_state(Registration.roommate_traits)
    await callback.message.answer("Какие качества для вас важны в руммейте?", reply_markup=ReplyKeyboardRemove())

@router.message(Registration.roommate_traits)
async def process_roommate_traits(message: Message, state: FSMContext):
    roommate_traits = message.text
    await state.update_data(roommate_traits=roommate_traits)
    await state.set_state(Registration.wishes)
    await message.answer("Есть ли у вас какие-либо особые пожелания или требования к руммейту?")

@router.message(Registration.wishes)
async def process_wishes(message: Message, state: FSMContext):
    wishes = message.text
    await state.update_data(wishes=wishes)
    data = await state.get_data()
    specialty = data['specialty']
    gender = data['gender']

    markup = await keyboards.room_keyboard(int(specialty), gender, page=1)
    await state.set_state(Registration.room)
    await message.answer('Выберите комнату:', reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith("pagination_"))
async def handle_pagination(callback_query: CallbackQuery, state: FSMContext):
    # Получаем номер страницы из callback_data
    page = int(callback_query.data.split("_")[1])
    data = await state.get_data()

    specialty_id = data.get("specialty")
    gender = data.get("gender")

    # Генерируем новую клавиатуру для текущей страницы
    keyboard = await keyboards.room_keyboard(specialty_id, gender, page)

    # Обновляем сообщение с новой клавиатурой
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()


# Обработка нажатии на кнопку "Назад"
@router.callback_query(lambda c: c.data == 'back')
async def process_back(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(Registration.faculty)

    await callback_query.message.answer('Выберите ваш факультет:', reply_markup=await keyboards.faculty_keyboard())

    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith('room_'))
async def register_room(callback_query: CallbackQuery, state: FSMContext):
    room = callback_query.data.split('_')[1]
    await state.update_data(room=room)
    print(f"{room} fefsfsf")
    #await state.update_data(room=room)
    await callback_query.message.edit_text(
        f"Вы выбрали комнату {room} для бронирования.",
        reply_markup=None  # Удаляем клавиатуру
    )
    list_roommates = await get_roommates(room)
    if len(list_roommates) > 0:
        for roommate in list_roommates:
            await callback_query.message.answer(str(roommate), reply_markup=keyboards.book)
    else:
        await callback_query.message.answer("В этой комнате пока нет студентов", reply_markup=keyboards.book)
    await callback_query.answer()



@router.message(F.text == 'Забронировать')
async def process_book(message: Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные из состояния
    room = data["room"]  # Получаем текущую комнату

    if not room:
        # Если комната не выбрана, просим выбрать
        await message.answer("Вы не выбрали комнату. Пожалуйста, выберите комнату перед бронированием.")
        return

    # Обновляем состояние с комнатой
    await state.update_data(room=room)

    # Переходим к следующему шагу
    await state.set_state(Registration.phone_number)
    await message.answer("Напишите номер телефона: ", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'Вернуться назад')
async def process_decline(message: Message, state: FSMContext):
    await state.set_state(Registration.room)
    # Получаем данные из состояния
    data = await state.get_data()
    specialty = data.get('specialty')
    gender = data.get('gender')

    # Убираем старое сообщение и клавиатуру
    await message.delete()
    await message.answer("Вы вернулись назад", reply_markup=ReplyKeyboardRemove())

    # Отправляем клавиатуру для выбора комнаты с данными specialty и gender
    await message.answer('Выберите комнату:', reply_markup=await keyboards.room_keyboard(int(specialty), gender))

# Обработка города
@router.message(Registration.phone_number)
async def register_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(Registration.city)
    await message.answer('Введите ваш город:')

# Завершение регистрации
@router.message(Registration.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()

    await post_user(data)
    start_time = datetime.now()

    # Запускаем таймер в фоновом режиме
    asyncio.create_task(start_timer(data["phone_number"], start_time))
    faculty = await get_faculty(data['faculty'])
    ru_gender = {
        "male": "Мужской",
        "female": "Женский"
    }
    specialty = await get_specialty_one((data['specialty']))
    await message.answer(f'Регистрация завершена!\n'
                         f'Фамилия: {data["surname"]}\n'
                         f'Имя: {data["name"]}\n'
                         f'Пол: {ru_gender[data["gender"]]}\n'
                         f'Факультет: {faculty.name}\n'
                         f'Специальность: {specialty.name}\n'
                         f'Город: {data["city"]}\n'
                         f'Комната: {data.get("room", "Не выбрана")}\n'
                         f'Номер телефона: {data.get("phone_number", "Не выбрана")}\n')

    await state.set_state(Registration.payment_accommodation)
    await message.answer("⚠️ВАЖНО! Если вы не отправите квитанции за оплату в течении тридцати минут, вам придется регистрироваться заново.⚠️\n\nСначала оплатите за проживание.\nЗа один семестр 234000,\nЗа учебный год 468000 тенге",
                         reply_markup=keyboards.payment_keyboard)


# Хендлер для получения информации о платеже за проживание


# Папка для хранения файлов
PAYMENTS_FOLDER = 'payments/'

# File save location

@router.message(Registration.payment_accommodation, F.content_type == ContentType.DOCUMENT)
async def handle_accommodation_payment_pdf(message: Message, state: FSMContext):

    data = await state.get_data()
    document = message.document

    # Ensure the folder exists
    os.makedirs(PAYMENTS_FOLDER, exist_ok=True)

    # File path
    file_path = os.path.join(PAYMENTS_FOLDER, document.file_name)

    new_file_name = f"accommodation_payment_{data["phone_number"]}.pdf"

    # File path
    file_path = os.path.join(PAYMENTS_FOLDER, new_file_name)

    # Download the file
    await bot.download(document.file_id, destination=file_path)

    # Save the file path in the FSM context
    await state.update_data(payment_accommodation=file_path)

    # Send response and update state
    await message.answer(
        "Чек за проживание получен.\n\nТеперь отправьте чек за еду.\nЗа один семестр 213750 тенге.\nЗа один учебный год 427500 тенге.",
        reply_markup=keyboards.food_payment_keyboard
    )
    await state.set_state(Registration.payment_food)


@router.message(Registration.payment_food, F.content_type == ContentType.DOCUMENT)
async def handle_food_payment_pdf(message: Message, state: FSMContext):
    data = await state.get_data()
    document = message.document

    # Ensure the folder exists
    os.makedirs(PAYMENTS_FOLDER, exist_ok=True)

    new_file_name = f"dinner_payment_{data["phone_number"]}.pdf"

    # File path
    file_path = os.path.join(PAYMENTS_FOLDER, new_file_name)

    # Download the file
    await bot.download(document.file_id, destination=file_path)

    # Save the file path in the FSM context
    await state.update_data(payment_food=file_path)
    data = await state.get_data()
    # Send confirmation
    await message.answer("""Чек за еду получен. Осталось только ждать ответа от нас!\n📄 Перечень документов для общежития:
· Удостоверение личности
· 075 и 063 форма, флюрография
· Чек за оплату
· 3x4 фото – 2 штук
· Доверенность (для несовершеннолетних)""")
    await update_payment_status(int(data["phone_number"]), str(data["payment_accommodation"]), str(data["payment_food"]))

    await state.set_state(Registration.is_approved_payment)

@router.message(Registration.is_approved_payment)
async def handle_is_approved_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(is_approved_payment=1)
    await state.clear()