from gi.repository import Gom
from loguru import logger

from todopatamus.models.todoitem import TodoItem
from todopatamus.services.db import DbService


class TodoService:
    def __init__(self, db_service: DbService):
        logger.debug("TodoService init")
        self.db_service = db_service
        self.repository = self.db_service.repository

        self.apply_migrations()

    def apply_migrations(self):
        logger.debug("TodoService begin migration")
        self.repository.automatic_migrate_sync(1, [TodoItem])
        logger.debug("TodoService migration completed")

    def get_todos(self):
        raise NotImplementedError()

    def get_todo(self, todo_id: str):
        return self.repository.find_one_sync(TodoItem, Gom.Filter.new_eq("id", todo_id))

    def put_todo(self, summary: str):
        item: TodoItem = TodoItem(repository=self.repository, summary=str)
        item.save_sync()
