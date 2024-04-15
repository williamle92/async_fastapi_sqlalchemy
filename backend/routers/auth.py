from fastapi import APIRouter, Depends
from backend.pydantic.auth import Token, OAuthRequestForm
from backend.models.base import get_connection
from sqlalchemy import select, and_, insert
from backend.models.users import User
from backend.pydantic.auth import RegisterIn, RegisterOut
from sqlalchemy.ext.asyncio import AsyncEngine
from passlib.context import CryptContext

router: APIRouter = APIRouter()


async def verify_password_hash(hash_password: str, password: str) -> bool:
	pass_context: CryptContext = CryptContext(schemes=["bcrypt"])
	return pass_context.verify(password, hash_password)


async def hash_password(password: str):
	pass_context: CryptContext = CryptContext(schemes=["bcrypt"])
	return pass_context.hash(password)


@router.post("/token", response_model=Token)
async def verify_token(
	data: OAuthRequestForm = Depends(OAuthRequestForm), connection=Depends(get_connection)
):
	async with connection.connect() as conn:
		user: User = await conn.execute(
			select(User).where(
				and_(User.email == data.username, User.hashed_password == data.password)
			)
		)
		result = user.fetch()
		if not result:
			pass


@router.post("/register", response_model=RegisterOut, status_code=200)
async def register(request: RegisterIn, engine: AsyncEngine = Depends(get_connection)):
	hashed_password: str = await hash_password(request.password)

	async with engine.connect() as conn:
		insert_user = await conn.execute(
			insert(User)
			.values(**request.model_dump(exclude="password"), hashed_password=hashed_password)
			.returning(
				User.first_name,
				User.last_name,
				User.email,
				User.id,
				User.permission,
				User.phone_number,
				User.phone_country_code,
			)
		)
		result = insert_user.first()
		await conn.commit()
		return RegisterOut(**result._asdict())
