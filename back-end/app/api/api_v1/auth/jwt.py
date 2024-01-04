from datetime import datetime
from typing import Any
from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from app.api.api_v1.deps.user_deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_access_token
from app.models.user_model import User
from app.schemas.auth_schema import TokenPayload, TokenSchema
from app.schemas.user_schema import UserOut
from app.services.user_service import UserService
from jose import jwt, JWTError

auth_router = APIRouter()


@auth_router.post("/login", summary="Create Access token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    # accept email from the frontend even though oauth flow specifys username
    user = await UserService.authenticate(
        email_as_username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect details"
        )
    # create token if user exist
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_access_token": create_refresh_access_token(user.user_id),
    }


@auth_router.post("/test-token", summary="Check token Validity", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user


@auth_router.post("/refresh", summary="Refresh user token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_Id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect details"
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_access_token": create_refresh_access_token(user.user_id),
    }
