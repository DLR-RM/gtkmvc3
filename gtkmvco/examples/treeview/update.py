# PYGTKMVC TreeView contribution sample
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

class Person(gtkmvc.Model):
    name = ''
    __observables__ = ('name',)

class Controller(gtkmvc.Controller):
    def register_adapters(self):
        gtkmvc.adapters.containers.watch_items_in_tree(self.view['liststore1'])
        self.setup_columns()

    def on_add_clicked(self, button):
        t = self.view['liststore1']
        m = Person()
        v = gtkmvc.View(builder='single.ui')
        c = gtkmvc.Controller(m, v, auto_adapt=True)
        t.append([m])

    def on_remove_clicked(self, button):
        # TODO move object lookup into view method.
        t, i = self.view['treeview1'].get_selection().get_selected()
        t.remove(i)

m = gtkmvc.Model()
v = gtkmvc.View(builder='update.ui')
c = Controller(m, v)

gtk.main()
