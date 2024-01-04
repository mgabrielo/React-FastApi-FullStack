from uuid import UUID
from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token:str
    refresh_access_token:str

class TokenPayload(BaseModel):
    sub:UUID = None
    exp: int = None