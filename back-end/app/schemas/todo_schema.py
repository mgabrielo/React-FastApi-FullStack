from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(..., title="Title", min_length=5, max_length=50)
    description: str = Field(..., title="Description", min_length=2, max_length=500)
    status: Optional[bool] = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(..., title="Title", min_length=5, max_length=50)
    description: Optional[str] = Field(
        ..., title="Description", min_length=2, max_length=500
    )
    status: Optional[bool] = False


class TodoOut(BaseModel):
    todo_id: UUID
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
