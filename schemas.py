from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from service import get_current_user_id

class UserLogMod(BaseModel):
    password: str
    username: str

class NoteAddMod(BaseModel):
    name: str
    discription: str

class NoteMod(NoteAddMod):
    userid: int
    model_config = ConfigDict(from_attributes=True)




IdSchema = Annotated[int, Depends(get_current_user_id)]