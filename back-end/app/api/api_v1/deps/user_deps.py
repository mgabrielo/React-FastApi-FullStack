from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.core.config import settings
from app.models.user_model import User
from jose import jwt, JWTError
from app.schemas.auth_schema import TokenPayload
from app.services.user_service import UserService

reuseable_outh=OAuth2PasswordBearer(
    tokenUrl= f'{settings.AP1_V1}/auth/login',
    scheme_name="JWT"
)

async def get_current_user(token:str = Depends(reuseable_outh))-> User:
    try:
        payload =jwt.decode(
            token, settings.JWT_SECRET,algorithms=[settings.ALGORITHM]
        )
        token_data=TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has Expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except (JWTError, ValidationError):
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="credentials could Not be validated",
                headers={"WWW-Authenticate": "Bearer"}
            )
    user= await UserService.get_user_by_Id(token_data.sub)

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User could Not be validated",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    return user

        
