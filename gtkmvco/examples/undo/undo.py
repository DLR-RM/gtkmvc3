# PYGTKMVC Undo contribution UI
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

import _importer

import locale
import random

import gtk

import gtkmvc

from undo_manager import UndoModel

def iternames():
    """
    Monday...Sunday
    """
    for i in range(2, 8) + [1]:
        yield locale.nl_langinfo(getattr(locale, 'DAY_%i' % i))

class Day(gtkmvc.Model):
    name = ''
    hours = 0
    __observables__ = ('name', 'hours')

def adapt_availability(model, name, widget):
    a = gtkmvc.adapters.Adapter(model, name)
    a.connect_widget(widget,
        getter=gtk.Widget.get_sensitive,
        setter=gtk.Widget.set_sensitive,
        signal='notify::sensitive')
    return a

def adapt_label(model, name, widget):
    a = gtkmvc.adapters.Adapter(model, name)
    a.connect_widget(widget,
        getter=gtk.Button.get_label,
        setter=gtk.Button.set_label,
        signal='notify::label')
    return a

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        self.undo = UndoModel()
        self.undo.register_observer(self)

        self.list = gtk.ListStore(object)

        for name in iternames():
            day = Day()
            day.name = name
            self.list.append([day])
            self.undo.observe_model(day)

        view['treeview1'].set_model(self.list)
        gtkmvc.adapters.containers.watch_items_in_tree(self.list)

    def on_button1__clicked(self, widget):
        self.undo.undo()

    def on_button2__clicked(self, widget):
        self.undo.redo()

    def on_button3__clicked(self, widget):
        self.undo.begin_grouping()
        for row in self.list:
            row[0].hours = int(random.random() * 10)
        self.undo.set_action_name("random hours")
        self.undo.end_grouping()

    def on_window1__delete_event(self, widget, event):
        gtk.main_quit()

    def register_adapters(self):
        self.setup_columns()

        adapt_availability(self.undo, 'undoable', self.view['button1'])
        adapt_availability(self.undo, 'redoable', self.view['button2'])
        adapt_label(self.undo, 'undo_label', self.view['button1'])
        adapt_label(self.undo, 'redo_label', self.view['button2'])

Controller(gtkmvc.Model(), gtkmvc.View(builder='undo.ui'), handlers='class')

gtk.main()
