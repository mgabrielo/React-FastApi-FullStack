from typing import Optional
from uuid import UUID
from app.models.user_model import User
from app.schemas.user_schema import UserAuth
from app.core.security import get_password, verify_password

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
       user_creation =User(
           username=user.username,
           email=user.email,
           hashed_password=get_password(user.password)
       )
       await user_creation.save()
       return user_creation
    
    @staticmethod
    async def authenticate(email_as_username:str, password:str)->Optional[User]:
        email_input=email_as_username
        user = await UserService.get_user_by_Email(email=email_input)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user

    @staticmethod 
    async def get_user_by_Email(email:str)->Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod 
    async def get_user_by_Id(id:UUID)->Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user
       