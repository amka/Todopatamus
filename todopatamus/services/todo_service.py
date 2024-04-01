import datetime
from typing import List

from gi.repository import Gom, GObject
from loguru import logger

from todopatamus.models.todoitem import TodoItem
from todopatamus.services.db import DbService


class TodoService(GObject.GObject):
    __gtype_name__ = "TodoService"

    __gsignals__ = {
        "todos-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, db_service: DbService):
        super().__init__()

        self._db_service = db_service
        logger.debug("TodoService init")
        self.db_service = db_service
        self.repository = self.db_service.repository

        self.apply_migrations()

    def apply_migrations(self):
        logger.debug("TodoService begin migration")
        self.repository.automatic_migrate_sync(1, [TodoItem])
        logger.debug("TodoService migration completed")

    def get_todos(self, page_number: int = 1, page_size: int = 30) -> List[TodoItem]:
        _filter = Gom.Filter.new_eq(TodoItem, "completed", False)
        _sorting: Gom.Sorting = Gom.Sorting(TodoItem, "createdAt", Gom.SortingMode.DESCENDING)

        group: Gom.ResourceGroup = self.repository.find_sorted_sync(TodoItem, filter=_filter, sorting=_sorting)
        group.fetch_sync(0, page_size)

        items: List[TodoItem] = []
        for item in group:
            items.append(item)

        return items

    def get_todo(self, todo_id: str):
        _filter = Gom.Filter.new_eq(TodoItem, "id", todo_id)
        return self.repository.find_one_sync(TodoItem, filter=_filter)

    def put_todo(self, todo: TodoItem):
        item: TodoItem = TodoItem(repository=self.repository, summary=todo.summary)
        item.todoId = todo.todoId
        item.completed = todo.completed
        item.createdAt = datetime.datetime.now(datetime.UTC).timestamp()
        item.updatedAt = datetime.datetime.now(datetime.UTC).timestamp()
        item.save_sync()

        self.emit("todos-changed", item.todoId)
