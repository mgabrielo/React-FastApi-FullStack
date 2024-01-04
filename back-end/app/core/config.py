from pydantic import AnyHttpUrl
from decouple import config
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    AP1_V1: str= "/api/v1"
    JWT_SECRET:str = config("JWT_SECRET", cast=str)
    JWT_REFRESH_SECRET:str = config("JWT_REFRESH_SECRET", cast=str)
    MONGODB_URI:str = config("MONGODB_URI", cast=str)
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRATION:int=45
    REFRESH_ACCESS_TOKEN_EXPIRATION:int=60 * 24 * 7
    PROJECT_NAME:str ="Auth-CRUD"
    CORS_ORIGINS:List[AnyHttpUrl] = []

    class Config:
        case_sensitive=True

settings =Settings()   