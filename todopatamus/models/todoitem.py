from gi.repository import Gom, GObject
from gi.types import GObjectMeta


class TodoItemResourceMeta(GObjectMeta):
    def __init__(cls, name, bases, dct):
        super(TodoItemResourceMeta, cls).__init__(name, bases, dct)
        cls.set_table("todo_items")
        cls.set_primary_key("todo_id")
        cls.set_notnull("summary")


class TodoItem(Gom.Resource, metaclass=TodoItemResourceMeta):
    todo_id = GObject.Property(type=str)
    # Short Summary
    summary = GObject.Property(type=str)
    # Long Summary
    body = GObject.Property(type=str)
    # Priority, default 1 means normal
    priority = GObject.Property(type=int, default=1)

    created_at = GObject.Property(type=int)
    modified_at = GObject.Property(type=int)

    completed = GObject.Property(type=bool, default=False)
    completed_at = GObject.Property(type=int)

    def __str__(self):
        return f'<TodoItem {self.todo_id}: {self.summary[:20]}>'
