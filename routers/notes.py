from typing import List

from fastapi import APIRouter
from DB.requests import add_notes, del_notes, upgrade_notes
from schemas import IdSchema, NoteAddMod, NoteMod
from service import insert_all_notes

router = APIRouter(
    tags=["notes"]
)


@router.get("/")
async def get_all(id: IdSchema, response_model=List[NoteMod]):
    result = await insert_all_notes(id)
    return result

@router.post("/add")
async def add_new_notes(data: NoteAddMod , id: IdSchema):
    result = await add_notes(data, id)
    return {"Body":f"{result}"}


@router.delete("/delete")
async def delete_notes(notes_id: int, user_id: IdSchema):
    result = await del_notes(notes_id, user_id)
    return {"Body":f"{result}"}

@router.put("/put")
async def put_notes(data: NoteAddMod, user_id: IdSchema,  id_notes: int):
    full_note = NoteMod(**data.model_dump(), userid=user_id)
    result = await upgrade_notes(full_note, id_notes)
    return {"Body":f"{result}"}
