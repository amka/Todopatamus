from gi.repository import Gom, GObject
from gi.types import GObjectMeta


class TodoItemResourceMeta(GObjectMeta):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.set_table("todo_items")
        cls.set_primary_key("todoId")
        cls.set_notnull("summary")
        cls.set_property_new_in_version('favorite', 2)


class TodoItem(Gom.Resource, metaclass=TodoItemResourceMeta):
    todoId = GObject.Property(type=str)
    # Short Summary
    summary = GObject.Property(type=str)
    # Long Summary
    body = GObject.Property(type=str)
    # Priority, default 1 means normal
    priority = GObject.Property(type=int, default=1)

    createdAt = GObject.Property(type=int)
    modifiedAt = GObject.Property(type=int)

    favorite = GObject.Property(type=bool, default=False)
    completed = GObject.Property(type=bool, default=False)
    completedAt = GObject.Property(type=int)

    def __str__(self):
        return f'<TodoItem {self.todoId}: {self.summary[:20]}>'
