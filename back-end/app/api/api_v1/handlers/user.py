from fastapi import APIRouter, HTTPException, status
from pymongo import errors
from app.schemas.user_schema import UserAuth, UserOut
from app.services.user_service import UserService

user_router = APIRouter()

@user_router.post('/create', summary="create new user", response_model=UserOut)
async def create_user(data:UserAuth):
    try:
        return await UserService.create_user(data)
    except errors.DuplicateKeyError :
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="User already Exist")
