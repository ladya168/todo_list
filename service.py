from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, status, Cookie, HTTPException
import jwt
from DB.db import create_all, drop_all
from config import settings


async def get_current_user_id(access_token: str | None = Cookie(None)) -> int:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не найден токен авторизации в cookies",
        )
    
    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        
        user_id: str | None = payload.get("sub") 
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный токен",
            )
        return int(user_id)
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
        )

async def create_token(id:int):
    payload ={
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

async def insert_all_notes(id: int) -> list :
    from DB.requests import get_all_notes
    result = []
    db_object = await get_all_notes(id)
    for object in db_object:
        result.append(object)
    return result

def identification(data):
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("dropping all tables")
    await drop_all()
    print("creating all tables")
    await create_all()
    yield
    print("App stopped")

