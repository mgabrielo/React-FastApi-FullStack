from beanie import init_beanie
from fastapi import FastAPI
from app.core.config import settings
from pymongo import MongoClient
from app.api.api_v1.route import router
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.todo_model import Todo

from app.models.user_model import User

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.AP1_V1}/openapi.json"
)


@app.on_event("startup")
async def initialize_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)

    await init_beanie(
        database=client.get_database("auth_crud"), document_models=[User, Todo]
    )


app.include_router(router, prefix=settings.AP1_V1)
