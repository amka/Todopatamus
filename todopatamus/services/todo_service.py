from typing import List

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

    def put_todo(self, summary: str):
        item: TodoItem = TodoItem(repository=self.repository, summary=str)
        item.save_sync()
