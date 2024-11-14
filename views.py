from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_button():
    language = InlineKeyboardBuilder()
    language.add(InlineKeyboardButton(text="KZ", callback_data="kz"))
    language.add(InlineKeyboardButton(text="RU", callback_data="ru"))
    reply_markup = language.as_markup()
    return reply_markup


def start(language):
    start_message = open(f'messages/start_message_{language}.txt')

    return start_message


def payment_button():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="ЖАТАХАНА ҮШІН", url="https://kaspi.kz/pay/_gate?action=service_with_subservice&service_id=2766&subservice_id=12178&region_id=18"),
        InlineKeyboardButton(text="ТАМАҚТАНУ ҮШІН", url="https://kaspi.kz/pay/_gate?action=service_with_subservice&service_id=2766&subservice_id=21871&region_id=18"),
    )
    reply_markup = keyboard_builder.as_markup()

    return reply_markup


def gender_button():
    gender = InlineKeyboardBuilder()
    gender.add(InlineKeyboardButton(text="Мужчина", callback_data="Мужчина"))
    gender.add(InlineKeyboardButton(text="Женщина", callback_data="Женщина"))
    reply_markup = gender.as_markup()

    return reply_markup


def rooms():
    room = InlineKeyboardBuilder()
    for i in range(10):
        room.add(InlineKeyboardButton(text=f"C{322+i}", callback_data=f"room"))
    room.adjust(2)
    reply_markup = room.as_markup()
    return reply_markup

