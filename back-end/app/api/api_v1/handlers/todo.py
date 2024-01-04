from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from app.api.api_v1.deps.user_deps import get_current_user
from app.models.todo_model import Todo
from app.models.user_model import User

from app.schemas.todo_schema import TodoCreate, TodoOut, TodoUpdate
from app.services.todo_service import TodoService

todo_router = APIRouter()


@todo_router.get("/", summary="get all todos", response_model=List[TodoOut])
async def get_all_todos(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todo(current_user)


@todo_router.post("/create", summary="create todo instance", response_model=Todo)
async def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(data, current_user)


@todo_router.get("/{todo_id}", summary="get one todo instance", response_model=TodoOut)
async def retrieve_todo(todo_id: UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.retrieve_todo(todo_id, current_user)


@todo_router.put(
    "/{todo_id}", summary="update one todo instance", response_model=TodoOut
)
async def update_todo(
    todo_id: UUID, todo_data: TodoUpdate, current_user: User = Depends(get_current_user)
):
    return await TodoService.update_todo(todo_id, todo_data, current_user)


@todo_router.delete(
    "/{todo_id}",
    summary="delete one todo instance",
)
async def delete_todo(todo_id: UUID, current_user: User = Depends(get_current_user)):
    await TodoService.delete_todo(todo_id, current_user)
    return None
