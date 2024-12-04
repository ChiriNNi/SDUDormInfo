from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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

class Specialty(Base):
    __tablename__ = 'specialities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    faculty: Mapped[int] = mapped_column(ForeignKey('faculties.id'))

class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(4))


# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)