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
from gi.repository import Gtk, GObject, Gio, GLib
from loguru import logger

from todopatamus.models.category import Category


@Gtk.Template(resource_path='/com/tenderowl/todopatamus/ui/sidebar-column.ui')
class SidebarColumn(Gtk.Box):
    __gtype_name__ = 'SidebarColumn'

    # Passed in template
    primary_menu = GObject.Property(type=Gio.Menu)

    selection_model: Gtk.SingleSelection = Gtk.Template.Child()
    categories: Gio.ListStore = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.setup_categories()
        self._on_category_activated(self.categories.get_item(0))

    def setup_categories(self):
        self.categories.remove_all()
        self.categories.append(Category(title='Inbox', icon_name='preferences-system-notifications-symbolic'))
        self.categories.append(Category(title='Favorite', icon_name='starred-symbolic'))
        self.categories.append(Category(title='Completed', icon_name='checkbox-checked-symbolic'))

    @Gtk.Template.Callback()
    def on_listview_activate(self, _list_view: Gtk.ListView, position: int):
        logger.debug(f'SidebarColumn.on_selection_changed: {position}')
        self.selection_model.set_selected(position)
        self._on_category_activated(self.categories.get_item(position))

    def _on_category_activated(self, category: Category):
        logger.debug(f'SidebarColumn._on_category_activated: {category}')
        self.activate_action('app.category-activate', GLib.Variant.new_string(category.name))
