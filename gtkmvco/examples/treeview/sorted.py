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

import gtk

import _importer
import gtkmvc

from sorting import *

class Person(gtkmvc.Model):
    name = ''
    age = 0
    __observables__ = ('name', 'age')

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        def add(name, age):
            p = Person()
            p.name = name
            p.age = age
            view['liststore'].append([p])
        add("Adam", 30)
        add("Zachary", 30)
        add("Berta", 20)
        add("Yolanda", 20)

    def register_adapters(self):
        self.setup_columns()

        s = self.view['sorting'] = SortingView()
        s.set_labels(dict(name="Nome", age="Eta"))
        s.set_order([
            {'reverse': False, 'key': 'age'},
            {'reverse': False, 'key': 'name'},
            ])
        self.view['frame'].add(s)

    def on_button__clicked(self, widget):
        set_sort_function(
            self.view['treemodelsort'],
            get_sort_function(self.view['sorting'].get_order())
            )

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

class Simple(Controller):
    def register_adapters(self):
        self.setup_columns()

        for c in self.view['treeview'].get_columns():
            c.set_clickable(True)
            setup_sort_column(c)
        for n in ('label1', 'frame', 'button'):
            self.view[n].set_visible(False)

m = gtkmvc.Model()
v = gtkmvc.View(builder='sorted.ui')
c = Controller(m, v, handlers='class')

m = gtkmvc.Model()
v = gtkmvc.View(builder='sorted.ui')
c = Simple(m, v, handlers='class')

gtk.main()
