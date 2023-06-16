import os.path
from datetime import datetime
from typing import List

from peewee import SqliteDatabase

from todopatamus.models.todo import Todo
from .db import DbService


class TodoService:
    def get_items(self) -> List[Todo]:
        """
        Return all items excluding archived.
        """
        return Todo.select().where(not Todo.is_archived).all()

    def get_item(self, item_id: str) -> Todo:
        return Todo.select().where(Todo.id == item_id).get()

    def put_item(self, todo: Todo) -> Todo:
        todo.created_at = datetime.utcnow()
        todo.updated_at = datetime.utcnow()
        return todo.save(force_insert=True)

    def remove_item(self, todo_id: str) -> int:
        todo = Todo.select().where(Todo.id == todo_id)
        if not todo:
            return 0

        return todo.delete_instance()


todo_service = TodoService()
