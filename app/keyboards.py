from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, or_

from app.database.models import Room, Specialty
from app.database.requests import async_session, get_faculties, get_specialty, get_room, get_booked_count

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Заполнить анкету 📝'),
    KeyboardButton(text='Информация о общежитии 🏠')]
],
                           resize_keyboard=True)

book = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Забронировать"),
    KeyboardButton(text="Вернуться назад")]
], resize_keyboard=True)


def sleep_keyboard():
    builder = InlineKeyboardBuilder()

    button1 = InlineKeyboardButton(text="До 22:00", callback_data="sleep_До 22:00")
    button2 = InlineKeyboardButton(text="22:00-00:00", callback_data="sleep_22:00-00:00")
    button3 = InlineKeyboardButton(text="После 00:00", callback_data="sleep_После 00:00")

    builder.add(button1, button2, button3)
    builder.adjust(1)

    return builder.as_markup()

def wake_keyboard():
    builder = InlineKeyboardBuilder()

    button1 = InlineKeyboardButton(text="До 6:00", callback_data="wake_До 6:00")
    button2 = InlineKeyboardButton(text="6:00–8:00", callback_data="wake_6:00–8:00")
    button3 = InlineKeyboardButton(text="После 8:00", callback_data="wake_После 8:00")

    builder.add(button1, button2, button3)
    builder.adjust(1)

    return builder.as_markup()

def noise_keyboard():
    builder = InlineKeyboardBuilder()

    button1 = InlineKeyboardButton(text="Мне важна полная тишина.", callback_data="silence_Мне важна полная тишина.")
    button2 = InlineKeyboardButton(text="Легкий шум не мешает.", callback_data="silence_Легкий шум не мешает.")
    button3 = InlineKeyboardButton(text="Я спокойно отношусь к шуму.", callback_data="silence_Я спокойно отношусь к шуму.")

    builder.add(button1, button2, button3)
    builder.adjust(1)

    return builder.as_markup()

def order_keyboard():
    builder = InlineKeyboardBuilder()

    button1 = InlineKeyboardButton(text="Очень важно,\n чтобы все было чисто.", callback_data="order_Очень важно.")
    button2 = InlineKeyboardButton(text="Я предпочитаю порядок,\n но могу мириться с беспорядком.", callback_data="order_Я предпочитаю порядок.")
    button3 = InlineKeyboardButton(text="Беспорядок меня не беспокоит.", callback_data="order_Беспорядок меня не беспокоит.")

    builder.add(button1, button2, button3)
    builder.adjust(1)

    return builder.as_markup()

def religion_keyboard():
    builder = InlineKeyboardBuilder()

    button1 = InlineKeyboardButton(text="Очень важно.", callback_data="religion_Очень важно.")
    button2 = InlineKeyboardButton(text="Было бы хорошо, но не обязательно.", callback_data="religion_Было бы хорошо.")
    button3 = InlineKeyboardButton(text="Мне все равно.", callback_data="religion_Мне все равно.")

    builder.add(button1, button2, button3)
    builder.adjust(1)

    return builder.as_markup()


def gender_keyboard():
    builder = InlineKeyboardBuilder()

    button_male = InlineKeyboardButton(text="Мужской 👨", callback_data="gender_male")
    button_female = InlineKeyboardButton(text="Женский 👩", callback_data="gender_female")

    builder.add(button_male, button_female)
    builder.adjust(1)

    return builder.as_markup()


async def faculty_keyboard():
    # faculties = [
    #     ("Инженерии и Естественных наук", "engineering"),
    #     ("Педагогики и Гуманитарных наук", "pedagogy"),
    #     ("Права и Социальных наук", "law"),
    #     ("Школа Бизнеса СДУ", "business")
    # ]

    faculties = await get_faculties()

    builder = InlineKeyboardBuilder()

    for faculty in faculties:
        builder.add(InlineKeyboardButton(text=faculty.name, callback_data=f'faculty_{faculty.id}'))

    builder.adjust(1)

    return builder.as_markup()


async def specialty_keyboard(faculty_id):
    builder = InlineKeyboardBuilder()

    # Маппинг факультетов на числовые коды
    # faculty_codes = {
    #     "engineering": 1,
    #     "pedagogy": 2,
    #     "law": 3,
    #     "business": 4
    # }

    # Специальности с короткими кодами
    # specialties = {
    #     1: [
    #         ("Информационные системы", "s1"),
    #         ("Информационные системы для бизнеса", "s2"),
    #         ("Компьютерные науки", "s3"),
    #         ("Математика", "s4"),
    #         ("Математическое и компьютерное моделирование", "s5"),
    #         ("Мультимедийные науки", "s6"),
    #         ("Программная инженерия", "s7"),
    #         ("Статистика и наука о данных", "s8")
    #     ],
    #     2: [
    #         ("Два иностранных языка", "s9"),
    #         ("Дошкольное обучение и воспитание", "s10"),
    #         ("Информатика", "s11"),
    #         ("История", "s12"),
    #         ("Казахский язык и литература", "s13"),
    #         ("Математика (педагогика)", "s14"),
    #         ("Педагогика и методика начального обучения", "s15"),
    #         ("Педагогика и Психология", "s16"),
    #         ("Переводческое дело", "s17"),
    #         ("Прикладная филология", "s18"),
    #         ("Социальная педагогика", "s19"),
    #         ("Физика и Информатика", "s20"),
    #         ("Химия и Биология", "s21")
    #     ],
    #     3: [
    #         ("Международное право", "s22"),
    #         ("Международные отношения", "s23"),
    #         ("Мультимедиа и телевизионная журналистика", "s24"),
    #         ("Право государственного управления", "s25"),
    #         ("Прикладная психология", "s26"),
    #         ("Прикладное право", "s27")
    #     ],
    #     4: [
    #         ("Диджитал маркетинг", "s28"),
    #         ("Менеджмент", "s29"),
    #         ("Учет и Аудит", "s30"),
    #         ("Финансы", "s31"),
    #         ("Экономика", "s32")
    #     ]
    # }

    specialities = await get_specialty(faculty_id);

    # Добавляем кнопки для каждой специальности
    for specialty in specialities:
        builder.add(InlineKeyboardButton(text=specialty.name, callback_data=f'specialty_{specialty.id}'))

    builder.add(InlineKeyboardButton(text="Назад", callback_data="back"))

    builder.adjust(1)  # Каждая кнопка на отдельной строке

    # Возвращаем клавиатуру
    return builder.as_markup()


async def room_keyboard(specialty_id: int, gender: str, page: int = 1, page_size: int = 10) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    async with async_session() as session:
        stmt = (
            select(Room)
            .join(Room.specialties)
            .where(Specialty.id == specialty_id)
        )

        if gender == 'male':
            stmt = stmt.where(
                or_(
                    Room.number.like("С%"),
                    Room.number.like("D%")
                )
            )
        else:
            stmt = stmt.where(
                or_(
                    Room.number.like("A%"),
                    Room.number.like("B%")
                )
            )

        result = await session.execute(stmt)
        rooms = result.scalars().all()

    # Пагинация
    total_rooms = len(rooms)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    rooms_on_page = rooms[start_index:end_index]

    for room in rooms_on_page:
        builder.add(InlineKeyboardButton(text=f"{room.number} {room.booked_count}/4 ", callback_data=f'room_{room.number}'))

    # Добавляем кнопки пагинации
    if page > 1:
        builder.add(InlineKeyboardButton(text="⬅ Назад", callback_data=f'pagination_{page - 1}'))
    if end_index < total_rooms:
        builder.add(InlineKeyboardButton(text="➡ Далее", callback_data=f'pagination_{page + 1}'))

    builder.adjust(2)  # Располагаем кнопки вертикально
    return builder.as_markup()

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить за проживание", callback_data="pay_accommodation", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F")]
    ]
)

# Пример клавиатуры для оплаты за еду
food_payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить за еду", callback_data="pay_food", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F")]
    ]
)