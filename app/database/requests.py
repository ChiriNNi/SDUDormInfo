import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import async_session, Room, User, RoomSpecialty
from app.database.models import Faculty, Specialty
from sqlalchemy import select

async def get_faculties():
    async with async_session() as session:
        return await session.scalars(select(Faculty))

async def get_faculty(faculty_id):
    async with async_session() as session:
        result =  await session.scalars(select(Faculty).where(Faculty.id == faculty_id))
        return result.first() if result else None
async def get_specialty(faculty_id):
    async with async_session() as session:
        return await session.scalars(select(Specialty).where(Specialty.faculty == faculty_id))

async def get_specialty_one(specialty_id):
    async with async_session() as session:
        result = await session.scalars(select(Specialty).where(Specialty.id == specialty_id))
        return result.first() if result else None
async def get_room():
    async with async_session() as session:
        return await session.scalars(select(Room).where(Room.booked_count < 4))

async def get_room_id_by_number(room_number):
    async with async_session() as session:
        # Query the room by its number
        room_result = await session.execute(
            select(Room).where(Room.number == room_number)
        )
        room = room_result.scalars().first()
        if room:
            return room.id  # Return the room_id
        else:
            return None

async def get_roommates(room_number):
    async with async_session() as session:
        # Get the room by number and eagerly load the users
        room_result = await session.execute(
            select(Room).where(Room.number == room_number).options(joinedload(Room.users))
        )
        room = room_result.scalars().first()
        print(f"Room {type(room_number)} found, users: {room.users}")
        if not room:
            return "Комната не найдена."

        # Make sure users are loaded before iterating
        if room.users:
            # Form the student list
            student_list = []
            count = 0
            for user in room.users:
                count += 1
                student_list.append( f"""*Руммейт {count}*
*Время сна*: {user.sleep_mode}\n
*Подъём*: {user.wake_up_time}\n
*Шум вечером*: {user.noise}\n
*Порядок в комнате*: {user.sleep_mode}\n
*Религиозные руммейты*: {user.religion}\n
*Качество будущих руммейтов*: {user.roommate_traits}\n
*Пожелания или требования руммейту*: {user.wishes}\n""")

        else:
            student_list = []
        return student_list

async def get_booked_count(room_number):
    async with async_session() as session:
        room_result = await session.execute(select(Room).where(Room.number == room_number))
        room = room_result.scalars().first()
        booked_count = room.booked_count
        return booked_count

async def post_room(user, room_number):
    async with async_session() as session:
        booked_count = await get_booked_count(room_number)
        print(f"book => {booked_count} and {booked_count + 1}")
        room_result = await session.execute(
            select(Room).where(Room.number == room_number)
        )
        room = room_result.scalars().first()
        print(f"room => {room} and {room.booked_count}")

        room.booked_count += 1


        await session.commit()

async def post_user(user):
    async with async_session() as session:
        # Create a User instance with data from the user dictionary
        room_id = await get_room_id_by_number(user.get("room"))
        new_user = User(
            surname=user["surname"],
            name=user["name"],
            gender=user["gender"],
            faculty=user["faculty"],
            speciality=user["specialty"],
            phone_number=user["phone_number"],
            city=user["city"],
            room_id=room_id,
            sleep_mode=user["sleep_mode"],
            wake_up_time=user["wake_up_time"],
            noise=user["noise_at_night"],
            order_room=user["order_room"],
            religion=user["religion"],
            roommate_traits=user["roommate_traits"],
            wishes=user["wishes"],
        )

        session.add(new_user)
        if user.get("room"):
            await post_room(new_user, user["room"])
        # Commit the session to save the new user to the database
        await session.commit()

        return new_user