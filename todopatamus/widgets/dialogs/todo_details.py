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
from gi.repository import Gtk, GObject, Adw

from todopatamus.models.todoitem import TodoItem
from todopatamus.widgets.todo_details import TodoDetails


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/todo-details-dialog.ui')
class TodoDetailsDialog(Adw.Dialog):
    __gtype_name__ = "TodoDetailsDialog"

    __gsignals__ = {
        'save': (GObject.SignalFlags.RUN_FIRST, None, (TodoItem,)),
        'cancel': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    header_bar: Adw.HeaderBar = Gtk.Template.Child()
    cancel_btn: Gtk.Button = Gtk.Template.Child()
    save_btn: Gtk.Button = Gtk.Template.Child()
    todo_details: TodoDetails = Gtk.Template.Child()

    readonly: bool = GObject.Property(type=bool, default=False)
    todo_item: TodoItem = GObject.Property(type=GObject.TYPE_PYOBJECT)

    def __init__(self, readonly: bool = False):
        super().__init__()

        self.readonly = readonly
        self.todo_details.readonly = readonly
        self.todo_details.todo_item = self.todo_item

    @Gtk.Template.Callback()
    def on_cancel_clicked(self, _sender: Gtk.Widget):
        self.emit('cancel')

    @Gtk.Template.Callback()
    def on_save_clicked(self, _sender: Gtk.Widget):
        self.emit('save', self.todo_details.todo_item)
