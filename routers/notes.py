from typing import List

from fastapi import APIRouter
from DB.requests import add_notes
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


