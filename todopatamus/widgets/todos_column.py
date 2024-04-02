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
from typing import List

from gi.repository import Adw, Gtk, Gio
from loguru import logger

from todopatamus.models.todoitem import TodoItem
from todopatamus.services.todo_service import TodoService
from todopatamus.widgets.todo_listitem import TodoListItem


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/todos-column.ui')
class TodosColumn(Adw.Bin):
    __gtype_name__ = "TodosColumn"

    todos_listview: Gtk.ListView = Gtk.Template.Child()
    todos: Gio.ListStore = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.todo_service: TodoService = Adw.Application.get_default().props.todo_service
        self.todo_service.connect('todos-changed', self._on_todos_changed)

        self.todos_listview.remove_css_class('view')

        self.load_todos()

    @Gtk.Template.Callback()
    def on_item_bind(self, factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        todo_item: TodoItem = list_item.get_item()
        todo_list_item: TodoListItem = list_item.get_child()
        todo_list_item.todo = todo_item

    @Gtk.Template.Callback()
    def on_item_setup(self, _factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        todo_list_item: TodoListItem = TodoListItem()
        list_item.set_child(todo_list_item)

    @Gtk.Template.Callback()
    def on_listview_activate(self, _list_view: Gtk.ListView, position: int):
        item: TodoItem = self.todos.get_item(position)
        dlg = Adw.Dialog()
        child = Adw.ToolbarView()
        child.add_top_bar(Adw.HeaderBar())
        child.set_content(Gtk.Label(label='TODO'))
        dlg.set_child(child)
        dlg.set_content_width(400)
        dlg.set_content_height(480)
        dlg.present(Gtk.Application.get_default().get_active_window())

    def load_todos(self):
        todos: List[TodoItem] = self.todo_service.get_todos()
        logger.debug(f"Loaded {len(todos)} todos")
        self.todos.remove_all()
        for todo in todos:
            self.todos.append(todo)

    def _on_todos_changed(self, _service: TodoService, todo_id: str):
        self.load_todos()
