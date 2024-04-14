from fastapi import FastAPI, Depends
from backend.models.users import User
from backend.models.base import get_connection
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.pydantic.users import UserOut, UsersOut
from sqlalchemy import select
from typing import List


app: FastAPI = FastAPI()


@app.get("/")
async def home():
    return {"hello": "world"}


@app.get("/users")
async def get_users(eng: AsyncEngine = Depends(get_connection)) -> UsersOut:
    async with eng.connect() as conn:
        users: List = await conn.execute(select(User))

        return UsersOut(users=[UserOut.model_validate(u) for u in users.fetchall()])
