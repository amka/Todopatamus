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
import nanoid
from gi.repository import Gtk, GObject
from loguru import logger

from todopatamus.models.todoitem import TodoItem


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/todo-entry.ui')
class TodoEntry(Gtk.Box):
    __gtype_name__ = "TodoEntry"

    __gsignals__ = {
        'create': (GObject.SignalFlags.RUN_FIRST, None, (TodoItem,)),
    }

    add_btn: Gtk.Button = Gtk.Template.Child()
    entry: Gtk.Entry = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.entry.grab_focus()

    def _create_todo(self):
        text = self.entry.get_text().strip()
        self._toggle_error_state(not text)
        if text:
            item = TodoItem()
            item.todoId = nanoid.generate(size=24)
            item.summary = text
            self.emit('create', item)
            self.entry.set_text('')
            logger.debug('Created todo: {}', text)

    def _toggle_error_state(self, enabled: bool):
        self.entry.add_css_class('error') if enabled else self.entry.remove_css_class('error')

    @Gtk.Template.Callback()
    def on_entry_activate(self, _: Gtk.Entry):
        self._create_todo()

    @Gtk.Template.Callback()
    def on_add_btn_clicked(self, _: Gtk.Button):
        self._create_todo()
