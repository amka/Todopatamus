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

    current_category: str = GObject.Property(type=str, default="inbox")

    def __init__(self, db_service: DbService):
        super().__init__()

        self._db_service = db_service
        logger.debug("TodoService init")
        self.db_service = db_service
        self.repository = self.db_service.repository

        self.apply_migrations()

    def apply_migrations(self):
        logger.debug("TodoService begin migration")
        self.repository.automatic_migrate_sync(2, [TodoItem])
        logger.debug("TodoService migration completed")

    def get_todos(self, page_number: int = 1, page_size: int = 30) -> List[TodoItem]:
        _filter: Gom.Filter = TodoService.get_filter_by_category(self.current_category)
        _sorting: Gom.Sorting = Gom.Sorting(TodoItem, "createdAt", Gom.SortingMode.DESCENDING)

        group: Gom.ResourceGroup = self.repository.find_sorted_sync(TodoItem, filter=_filter, sorting=_sorting)
        group.fetch_sync((page_number - 1) * page_size, page_size)
        return group

    def get_todo(self, todo_id: str) -> TodoItem:
        logger.debug(f"TodoService get_todo {todo_id}")
        _filter = Gom.Filter.new_eq(TodoItem, "todoId", todo_id)
        return self.repository.find_one_sync(TodoItem, filter=_filter)

    def put_todo(self, todo: TodoItem) -> TodoItem:
        logger.debug(f"TodoService put_todo {todo.todoId}")
        item: TodoItem = TodoItem(repository=self.repository, summary=todo.summary)
        item.todoId = todo.todoId
        item.completed = todo.completed
        item.createdAt = datetime.datetime.now(datetime.UTC).timestamp()
        item.modifiedAt = datetime.datetime.now(datetime.UTC).timestamp()
        item.save_sync()

        self.emit("todos-changed", item.todoId)

        return item

    def toggle_completed(self, todo_id: str, completed: bool) -> TodoItem:
        logger.debug(f"TodoService toggle_completed {todo_id} {completed}")
        item = self.get_todo(todo_id)
        item.completed = completed
        item.modifiedAt = datetime.datetime.now(datetime.UTC).timestamp()
        if completed:
            item.completedAt = datetime.datetime.now(datetime.UTC).timestamp()
        else:
            item.completedAt = -1
        item.save_sync()

        self.emit("todos-changed", item.todoId)
        return item

    def set_current_category(self, name: str):
        logger.debug(f"TodoService set_current_category {name}")
        self.current_category = name
        self.emit("todos-changed", name)

    @staticmethod
    def get_filter_by_category(category: str) -> Gom.Filter:
        match category:
            # Favorite, not completed
            case "favorite":
                return Gom.Filter.new_and(
                    Gom.Filter.new_eq(TodoItem, "favorite", True),
                    Gom.Filter.new_eq(TodoItem, "completed", False),
                )
            # All Completed
            case "completed":
                return Gom.Filter.new_eq(TodoItem, "completed", True)
            # Inbox, not completed, not favorite
            case _:
                return Gom.Filter.new_eq(TodoItem, "completed", False)
