from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Insert, Replace
from pydantic import Field, EmailStr
from typing import Optional
from app.models.user_model import User


class Todo(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = True
    title: Indexed(str)
    description: Indexed(str)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[User]

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __repr__(self) -> str:
        return {self.email}

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @before_event([Replace, Insert])
    def update_updated_at(self):
        self.updated_at = datetime.now()

    class Settings:
        name = "todos"
