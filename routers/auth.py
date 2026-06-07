from fastapi import APIRouter, HTTPException, Response
from DB.requests import add_user, check_user_exists
from schemas import UserLogMod
from service import create_token

router = APIRouter(
    tags=["auth"]
)

@router.post("/reg")
async def reg_user(creds: UserLogMod, response: Response):
    result = await add_user(creds)
    if result:
        token = await create_token(result)
        response.set_cookie("access_token", token)
        return {f"my_access_token":f"{token}"}
    raise HTTPException

@router.get("/login")
async def login_user(creds: UserLogMod, response: Response):
    result = await check_user_exists(creds)
    if result:
        token = await create_token(result.id)
        response.set_cookie("access_token", token)
        return {"my_access_token":f"{token}"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

