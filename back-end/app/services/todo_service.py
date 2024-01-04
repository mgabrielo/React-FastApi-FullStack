from typing import List
from uuid import UUID
from app.models.todo_model import Todo
from app.models.user_model import User
from app.schemas.todo_schema import TodoCreate, TodoUpdate


class TodoService:
    @staticmethod
    async def list_todo(user: User) -> List[Todo]:
        todos = await Todo.find(Todo.owner.id == user.id).to_list()
        return todos

    @staticmethod
    async def create_todo(data: TodoCreate, user: User) -> Todo:
        todo = Todo(**data.dict(), owner=user)
        return await todo.insert()

    @staticmethod
    async def retrieve_todo(todo_id: UUID, user: User) -> Todo:
        todo = await Todo.find_one(Todo.todo_id == todo_id, Todo.owner.id == user.id)
        return todo

    @staticmethod
    async def update_todo(todo_id: UUID, todo_data: TodoUpdate, user: User):
        todo = await TodoService.retrieve_todo(todo_id=todo_id, user=user)
        await todo.update({"$set": todo_data.dict(exclude_unset=True)})
        await todo.save()
        return todo

    @staticmethod
    async def delete_todo(todo_id: UUID, user: User):
        todo = await TodoService.retrieve_todo(todo_id=todo_id, user=user)
        if todo:
            await todo.delete()
        return None
