from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start():
    start_message = open('messages/start_message.txt')

    return start_message


def payment_button():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="ЖАТАХАНА ҮШІН", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F"),
        InlineKeyboardButton(text="ТАМАҚТАНУ ҮШІН", url="https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D1%8F"),
    )
    reply_markup=keyboard_builder.as_markup()

    return reply_markup


def gender_button():
    gender = InlineKeyboardBuilder()
    gender.add(InlineKeyboardButton(text="Мужчина", callback_data="option_1"))
    gender.add(InlineKeyboardButton(text="Женщина", callback_data="option_2"))
    reply_markup=gender.as_markup()

    return reply_markup