from aiogram.fsm.state import StatesGroup, State


class StudentInfo(StatesGroup):
    chat_id = State()
    waiting_for_full_name = State()
    waiting_for_gender = State()
    waiting_for_course = State()
    waiting_for_city = State()
    waiting_for_speciality = State()
