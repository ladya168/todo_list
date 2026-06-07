from sqlalchemy import select
from DB.db import Notes, Session, Users
from schemas import NoteMod, UserLogMod



async def add_user(creds: UserLogMod):
    async with Session() as session:
        creds_d = creds.model_dump()
        query = Users(**creds_d)
        session.add(query)
        await session.flush()
        user_id = query.id 
        await session.commit()
        return user_id

async def check_user_exists(creds: UserLogMod):
    async with Session() as session:
        creds_d = creds.model_dump()
        query = select(Users).filter_by(**creds_d)
        result = await session.execute(query)
        return result.scalars().first()

async def get_all_notes(id: int):
    async with Session() as session:
        query = select(Notes).where(Notes.userid == id)
        result = await session.execute(query)
        return result.scalars().all()


async def add_notes(data: NoteMod, user_id: int): 
    full_note = NoteMod(**data.model_dump(), userid=user_id)
    async with Session() as session:
        data_d = full_note.model_dump()
        query = Notes(**data_d)
        session.add(query)
        await session.flush()
        note_id = query.id 
        await session.commit()
        return note_id

