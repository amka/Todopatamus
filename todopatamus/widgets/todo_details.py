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


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/todo-details.ui')
class TodoDetails(Gtk.Box):
    __gtype_name__ = "TodoDetails"

    __gsignals__ = {
        'create': (GObject.SignalFlags.RUN_FIRST, None, (TodoItem,)),
    }

    summary_entry: Gtk.Entry = Gtk.Template.Child()
    body_entry: Gtk.TextView = Gtk.Template.Child()
    priority_dropdown: Gtk.DropDown = Gtk.Template.Child()

    _readonly: bool = False
    _todo_item: TodoItem = None

    def __init__(self, readonly: bool = False):
        super().__init__()

        self.readonly = readonly
        self.summary_entry.bind_property('sensitive', self, 'readonly', GObject.BindingFlags.INVERT_BOOLEAN)
        self.priority_dropdown.bind_property('sensitive', self, 'readonly', GObject.BindingFlags.INVERT_BOOLEAN)
        self.body_entry.bind_property('sensitive', self, 'readonly', GObject.BindingFlags.INVERT_BOOLEAN)
        # self.summary_entry.grab_focus()
        # self.summary_entry.select_region(0, 0)

    @GObject.Property(type=bool, default=False)
    def readonly(self) -> bool:
        return self._readonly

    @readonly.setter
    def readonly(self, value: bool):
        self._readonly = value

    @GObject.Property(type=GObject.TYPE_PYOBJECT)
    def todo_item(self):
        self._todo_item.summary = self.summary_entry.get_text()
        self._todo_item.priority = self.priority_dropdown.get_selected()
        buffer: Gtk.TextBuffer = self.body_entry.get_buffer()
        self._todo_item.body = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        return self._todo_item

    @todo_item.setter
    def todo_item(self, value: TodoItem):
        if not value:
            return

        self._todo_item = value
        self.summary_entry.set_text(value.summary)
        self.priority_dropdown.set_selected(self._todo_item.priority)
        self.body_entry.get_buffer().set_text(value.body)
