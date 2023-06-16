from peewee import BooleanField, TextField, CharField, SmallIntegerField, DateField

from .base import BaseModel


class Todo(BaseModel):
    summary = CharField()
    content = TextField(null=True)

    importance = SmallIntegerField(default=1)
    deadline_at = DateField(null=True)

    is_archived = BooleanField(default=False)
    is_done = BooleanField(default=False)
