# MIT License
#
# Copyright (c) 2024 Andrey Maksimov
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

from gi.repository import Adw
from gi.repository import Gtk

from todopatamus.models.todoitem import TodoItem
from todopatamus.services.todo_service import TodoService
from todopatamus.widgets.todo_entry import TodoEntry
from todopatamus.widgets.todos_column import TodosColumn


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/window.ui')
class TodopatamusWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TodopatamusWindow'

    todos_column: TodosColumn = Gtk.Template.Child()
    todo_entry: TodoEntry = Gtk.Template.Child()

    def __init__(self, application: Adw.Application, **kwargs):
        super().__init__(application=application, **kwargs)

        self.todo_service: TodoService = application.props.todo_service

        if Gtk.Application.get_default().props.profile == 'dev':
            self.add_css_class('devel')

        self.todo_entry.grab_focus()
        self.todo_entry.connect('create', self.on_todo_create)

    def on_todo_create(self, _entry: TodoEntry, todo: TodoItem):
        self.todo_service.put_todo(todo)
        self.todo_entry.grab_focus()
