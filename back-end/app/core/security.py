from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

password_context =CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password:str) -> str:
    return password_context.hash(password)

def verify_password(password:str, hashed_password:str) -> bool :
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta:int =None)->str:
    if expires_delta is not None:
        expires_delta= datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)
    
    to_encode ={"exp":expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, settings.ALGORITHM)
    return encoded_jwt

def create_refresh_access_token(subject: Union[str, Any], expires_delta:int =None)->str:
    if expires_delta is not None:
        expires_delta= datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_ACCESS_TOKEN_EXPIRATION)
    
    to_encode ={"exp":expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET, settings.ALGORITHM)
    return encoded_jwt


