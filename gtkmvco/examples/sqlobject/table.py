# PYGTKMVC SQLObject sample
# Copyright (C) 2013  Tobias Weber
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
Show two tree views, backed by a database. The left is fully editable,
the right mirrors changes.
"""

import _importer

import gtk
import sqlobject
from sqlobject import events

import gtkmvc

class TableStore(gtk.ListStore):
    def __init__(self, cls):
        """
        Represent all rows of the :class:`SQLObject` passed, at all times.

        This causes them to remain in memory, so use with care.
        """
        gtk.ListStore.__init__(self, object)

        events.listen(self.__on_updated, cls, events.RowUpdatedSignal)
        events.listen(self.__on_created, cls, events.RowCreatedSignal)
        events.listen(self.__on_destroy, cls, events.RowDestroySignal)

        for obj in cls.select():
            self.append((obj,))

    def __iter(self, obj):
        # TODO copy caching from adapters.containers.watch_items_in_tree
        i = self.get_iter_first()
        while i:
            if self.get_value(i, 0) is obj:
                return i
            i = self.iter_next(i)

    def __on_updated(self, obj, arg):
        i = self.__iter(obj)
        self.row_changed(self.get_path(i), i)

    def __on_created(self, obj, *args):
        self.append((obj,))

    def __on_destroy(self, obj, arg):
        i = self.__iter(obj)
        self.remove(i)

class Person(sqlobject.SQLObject):
    name = sqlobject.UnicodeCol()

class Controller(gtkmvc.Controller):
    handlers='class'

    def register_view(self, view):
        model = TableStore(Person)
        view['treeview'].set_model(model)
        view['treeview1'].set_model(model)

        self.setup_column('left', attribute='name', model=model)
        self.setup_column('right', attribute='name')

    def on_add__clicked(self, widget):
        Person(name="New")

    def on_remove__clicked(self, widget):
        t, i = self.view['treeview'].get_selection().get_selected()
        t.get_value(i, 0).destroySelf()

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

if __name__ == '__main__':
    sqlobject.sqlhub.processConnection = sqlobject.connectionForURI('sqlite:/:memory:')
    Person.createTable()

    Person(name="John")

    Controller(gtkmvc.Model(), gtkmvc.View(builder='table.ui'))
    gtk.main()