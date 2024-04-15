from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from typing import List
from backend.models import User
from backend.models.base import get_connection
from backend.pydantic.users import UserOut, UsersOut


router: APIRouter = APIRouter()


@router.get("/users")
async def get_users(eng: AsyncEngine = Depends(get_connection)) -> UsersOut:
	async with eng.connect() as conn:
		users: List = await conn.execute(select(User))

		return UsersOut(users=[UserOut.model_validate(u) for u in users.fetchall()])
