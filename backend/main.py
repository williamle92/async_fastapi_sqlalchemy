from fastapi import FastAPI
from backend.routers.users import router as user_router
from backend.routers.auth import router as auth_router

app: FastAPI = FastAPI()


app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def home():
	return {"hello": "world"}
