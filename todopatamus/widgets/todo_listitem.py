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

from gi.repository import Gtk, GObject

from todopatamus.models.todoitem import TodoItem


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/todo-listitem.ui')
class TodoListItem(Gtk.Box):
    __gtype_name__ = "TodoListItem"

    _todo: TodoItem = None

    completed_btn: Gtk.Button = Gtk.Template.Child()
    summary_label: Gtk.Label = Gtk.Template.Child()
    favorite_btn: Gtk.Button = Gtk.Template.Child()
    view_more_btn: Gtk.Button = Gtk.Template.Child()

    def __init__(self, todo: TodoItem = None):
        super().__init__()

        if todo is not None:
            self._update_ui(todo)

    def _update_ui(self, todo):
        completed_icon_name = 'checkbox-checked-symbolic' if todo.completed else 'checkbox-symbolic'
        self.completed_btn.set_icon_name(completed_icon_name)
        self.summary_label.set_markup(todo.summary)

    @GObject.Property(type=GObject.TYPE_PYOBJECT)
    def todo(self):
        return self._todo

    @todo.setter
    def todo(self, todo: TodoItem):
        self._todo = todo
        self._update_ui(todo)
