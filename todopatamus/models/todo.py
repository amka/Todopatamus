# MIT License
#
# Copyright (c) 2023 Andrey Maksimov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# SPDX-License-Identifier: MIT
from datetime import datetime, date
from enum import Enum

from gi.repository import GObject


class TodoType(Enum):
    TASK = 1
    NOTE = 2


class Todo(GObject.GObject):
    __gtype_name__ = 'Todo'

    __id: str
    __project_id: str
    __summary: str
    __content: str
    __todo_type: TodoType = TodoType.TASK

    __importance: int
    __deadline_at: date

    __created_at: datetime
    __modified_at: datetime
    __is_archived: bool = False

    def __init__(self):
        super().__init__()

    @GObject.Property(type=str)
    def identifier(self) -> str:
        return self.__id

    @GObject.Property(type=str)
    def project_id(self) -> str:
        return self.__project_id

    @GObject.Property(type=str)
    def summary(self) -> str:
        return self.__summary

    @GObject.Property(type=str)
    def content(self) -> str:
        return self.__content

    @GObject.Property(type=TodoType)
    def todo_type(self):
        return self.__todo_type

    @GObject.Property(type=date)
    def deadline_at(self) -> date:  # type: ignore
        return self.__deadline_at

    @GObject.Property(type=int)
    def importance(self) -> int:  # type: ignore
        return self.__importance

    @GObject.Property(type=datetime)
    def created_at(self) -> datetime:  # type: ignore
        return self.__created_at

    @GObject.Property(type=datetime)
    def modified_at(self) -> datetime:  # type: ignore
        return self.__modified_at

    @GObject.Property(type=bool)
    def is_archived(self) -> bool:
        return self.__is_archived

    def __repr__(self):
        return 'Todo Object `{0}` from Project {1}'.format(
            self.__summary,
            self.__project_id
        )

    def to_dict(self) -> dict:
        return {
            'id': self.identifier,
            'project_id': self.project_id,
            'summary': self.summary,
            'type': self.todo_type,
            'content': self.content,
            'importance': self.importance,
            'deadline_at': self.deadline_at,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'is_archived': self.is_archived,
        }
