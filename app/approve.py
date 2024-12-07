import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User, async_session, Room

TIME_LIMIT = timedelta(minutes=1)

async def update_payment_status(phone_number: int, payment_accommodation: str, payment_food: str):
    async with async_session() as session:
        try:
            # Находим пользователя по ID
            result = await session.execute(select(User).filter(User.phone_number == phone_number))


            user = result.scalar_one_or_none()
            if user:
                # Обновляем статус подтверждения оплаты
                user.is_payment_approved = 1
                user.payment_accommodation = payment_accommodation
                user.payment_food = payment_food
                await session.commit()
            else:
                print("jkjkljl")
        except Exception as e:
            print(f"Error updating payment status for user")

async def delete_user_by_phone_number(phone_number):
    async with async_session() as session:
        try:
            # Поиск пользователя по ID
            result = await session.execute(select(User).filter(User.phone_number == phone_number))
            user = result.scalar_one_or_none()
            result_room = await session.execute(select(Room).filter(Room.id == user.room_id))
            room = result_room.scalar_one_or_none()
            if user:
                if user.is_payment_approved == 0:
                    room.booked_count -= 1
                    await session.delete(user)
                    await session.commit()
        except Exception as e:
            print("OOUUU")

async def start_timer(phone_number: int, start_time: datetime):
    # Вычисление оставшегося времени
    elapsed_time = datetime.now() - start_time
    remaining_time = TIME_LIMIT - elapsed_time

    # Если прошло больше 30 минут
    if remaining_time <= timedelta(seconds=0):
        # Удаляем пользователя из базы данных
        await delete_user_by_phone_number(phone_number)


    else:
        # Ждем оставшееся время и затем удаляем пользователя
        await asyncio.sleep(remaining_time.total_seconds())
        await delete_user_by_phone_number(phone_number)
