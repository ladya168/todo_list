from sqlalchemy import select
from DB.db import Notes, Session, Users
from schemas import NoteAddMod, NoteMod, UserLogMod
from service import identification



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

async def del_notes(id_notes: int, id_user: int):
    async with Session() as session:
        query = select(Notes).where(Notes.id == id_notes)
        notes = await session.execute(query)
        result = notes.scalars().one_or_none()

        identification(result)

        await session.delete(result)
        await session.commit()
        return id
    

async def upgrade_notes(data: NoteMod, id: int):
    async with Session() as session:
        query = select(Notes).where(Notes.id == id).where(Notes.userid == data.userid)
        old_notes = (await session.execute(query)).scalars().one_or_none()

        identification(old_notes)

        data_d = data.model_dump()
        for key, value in data_d.items():
            if value:
                setattr(old_notes, key, value)
        await session.commit()
        return id




