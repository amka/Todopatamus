import nanoid
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
    summary = GObject.Property(type=str)
