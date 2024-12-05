from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Faculty(Base):
    __tablename__ = 'faculties'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    code: Mapped[str] = mapped_column(String(25))

class RoomSpecialty(Base):
    __tablename__ = 'room_specialty'

    room_id = mapped_column(ForeignKey('rooms.id'), primary_key=True)
    specialty_id = mapped_column(ForeignKey('specialities.id'), primary_key=True)

class Specialty(Base):
    __tablename__ = 'specialities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    faculty: Mapped[int] = mapped_column(ForeignKey('faculties.id'))
    rooms = relationship('Room', secondary='room_specialty', back_populates='specialties')


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(4), unique=True)
    booked_count = mapped_column(Integer, default=0)
    users = relationship("User", back_populates="room")
    specialties = relationship('Specialty', secondary='room_specialty', back_populates='rooms')




class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, default=0)
    surname = mapped_column(String)
    name = mapped_column(String)
    gender = mapped_column(String)
    faculty = mapped_column(ForeignKey('faculties.id'))
    speciality = mapped_column(ForeignKey('specialities.id'))
    course = mapped_column(Integer)
    city = mapped_column(String)
    room_id = mapped_column(Integer, ForeignKey('rooms.id'))
    room = relationship("Room", back_populates="users")

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)