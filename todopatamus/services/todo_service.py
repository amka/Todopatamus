from gi.overrides import Gom

from models.todoitem import TodoItem
from services.db import DbService


class TodoService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service
        self.repository = Gom.Repository(adapter=db_service.adapter)
        self.repository.automatic_migrate_sync(1, [TodoItem])

    def get_todos(self):
        raise NotImplementedError()

    def get_todo(self, todo_id: str):
        return self.repository.find_one_sync(TodoItem, Gom.Filter.new_eq("id", todo_id))

    def put_todo(self, summary: str):
        item: TodoItem = TodoItem(repository=self.repository, summary=str)
        item.save_sync()
