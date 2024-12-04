from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import async_session, Room
from app.database.models import Faculty, Specialty
from sqlalchemy import select

async def get_faculties():
    async with async_session() as session:
        return await session.scalars(select(Faculty))

async def get_specialty(faculty_id):
    async with async_session() as session:
        return await session.scalars(select(Specialty).where(Specialty.faculty == faculty_id))

async def get_room():
    async with async_session() as session:
        return await session.scalars(select(Room))