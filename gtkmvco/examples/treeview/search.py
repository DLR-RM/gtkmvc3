# PYGTKMVC TreeView contribution UI
# Copyright (C) 2011  Tobias Weber
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.

"""
Start typing to jump to a row.
"""

import gtk

import _importer
import gtkmvc

class Row(gtkmvc.Model):
    name = ''
    __observables__ = ['name']

def NameStore():
    s = gtk.ListStore(object)
    for name in dir(__builtins__):
        r = Row()
        r.name = name
        s.append([r])
    return s

def search_equal_func(model, column, key, iter, data):
    value = getattr(model.get_value(iter, column), data)
    # Case-sensitive.
    return key not in value

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view['treeview'].set_model(NameStore())
        view.show()

    def register_adapters(self):
        self.setup_columns()
        self.view['treeview'].set_search_equal_func(search_equal_func, 'name')

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

Controller(
    gtkmvc.Model(),
    gtkmvc.View(builder='search.ui', top='window'),
    handlers='class')
gtk.main()
