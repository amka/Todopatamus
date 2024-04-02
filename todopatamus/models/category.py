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

from gi.repository import GObject


class Category(GObject.GObject):
    __gtype_name__ = 'Category'

    name: str = GObject.Property(type=str, default='inbox')
    title: str = GObject.Property(type=str)
    description: str = GObject.Property(type=str)
    icon_name: str = GObject.Property(type=str)
    action_name: str = GObject.Property(type=str)

    def __init__(self, title: str = None,
                 name: str = None,
                 description: str = None,
                 icon_name: str = None,
                 action_name: str = None):
        """
        :param title: Title of the category
        :param name: Name of the category. If no name is given, it will be derived from the title.
        :param description: Description of the category
        :param icon_name: Icon name of the category
        :param action_name: Action name of the category
        """
        super().__init__()

        self.title = title
        self.description = description
        self.icon_name = icon_name
        self.action_name = action_name
        self.name = name or self.title
        if self.name:
            self.name = self.name.lower()

    def __str__(self):
        return f'<Category {self.title}>'
