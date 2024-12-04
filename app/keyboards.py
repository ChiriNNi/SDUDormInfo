from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_faculties, get_specialty, get_room

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Заполнить анкету 📝'),
    KeyboardButton(text='Информция о общежитии 🏠')]
],
                           resize_keyboard=True)

def gender_keyboard():
    builder = InlineKeyboardBuilder()

    button_male = InlineKeyboardButton(text="Мужской 👨", callback_data="gender_male")
    button_female = InlineKeyboardButton(text="Женский 👩", callback_data="gender_female")

    builder.add(button_male, button_female)
    builder.adjust(2)

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

    # Получаем список специальностей для выбранного факультета
    # faculty_specialties = specialties.get(faculty_codes.get(faculty_code), [])

    # Добавляем кнопки для каждой специальности
    for specialty in specialities:
        builder.add(InlineKeyboardButton(text=specialty.name, callback_data="specialty_"))

    builder.add(InlineKeyboardButton(text="Назад", callback_data="back"))

    builder.adjust(1)  # Каждая кнопка на отдельной строке

    # Возвращаем клавиатуру
    return builder.as_markup()

async def room_keyboard():
    builder = InlineKeyboardBuilder()
    rooms = await get_room();
    for room in rooms:
        builder.add(InlineKeyboardButton(text=room.number, callback_data=f'room_{room.number}'))
    builder.adjust(1)
    return builder.as_markup()
