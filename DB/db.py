from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from config import settings

engine = create_async_engine(settings.db_url)
Session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users" 
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str]
    username: Mapped[str]

class Notes(Base):
    __tablename__ = "notes" 
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    discription: Mapped[str]
    userid: Mapped [int]

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)