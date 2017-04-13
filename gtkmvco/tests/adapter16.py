"""
Test shows a button, a list and an entry. The entry should always reflect the
list selection. The button should change a random list item.

This is a real-world example of dot-notation Adapters with automatic intermediate
observing.
"""

import random
import re

import gtk

import _importer
import gtkmvc

class Selection(gtkmvc.adapters.basic.Adapter):
    def __init__(self, model, prop_name, empty):
        if not getattr(model, prop_name):
            setattr(model, prop_name, empty)
        self.empty_model = empty
        gtkmvc.adapters.basic.Adapter.__init__(self, model, prop_name)

    def connect_widget(self, treeview):
        sel = treeview.get_selection()
        def getter(s):
            tree_model, iter = s.get_selected()
            if iter:
                return tree_model[iter][0]
            else:
                return self.empty_model
        def setter(s, v):
            pass
        gtkmvc.adapters.basic.Adapter.connect_widget(self, sel,
            getter, setter, "changed")

class Person(gtkmvc.Model):
    name = None
    __observables__ = ("name",)

    def __init__(self, name):
        gtkmvc.Model.__init__(self)
        self.name = name

    def lengthen(self):
        self.name = re.sub(r'(?i)([aeiou])', r'\1\1', self.name, 1).capitalize()

class AddressBook(gtkmvc.Model):
    selected = None
    __observables__ = ("selected",)

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.tree_model = gtk.ListStore(object)

    def add(self, person):
        person.register_observer(self)
        self.tree_model.append([person])

    def property_name_value_change(self, person, old, new):
        for r in self.tree_model:
            if r[0] is person:
                self.tree_model.row_changed(r.path, r.iter)

    def doodle(self):
        r = random.choice(self.tree_model)
        r[0].lengthen()

class View(gtkmvc.View):
    def __init__(self):
        gtkmvc.View.__init__(self)

        w = self['window'] = gtk.Window()
        b = self['touch'] = gtk.Button("Doodle")
        t = self['tree'] = gtk.TreeView()
        e = self['name'] = gtk.Entry()
        v = gtk.VBox()
        v.pack_start(b)
        v.pack_start(t)
        v.pack_start(e)
        w.add(v)
        w.set_title("Inspect")
        w.set_default_size(200, 100)
        w.show_all()

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view['window'].connect('delete-event', self.on_window_delete_event)
        view['touch'].connect('clicked', self.on_button_clicked)

    def register_adapters(self):
        a = Selection(self.model, "selected", Person(""))
        a.connect_widget(self.view["tree"])
        self.adapt(a)

        self.adapt("selected.name", "name")

        self.setup_columns()

    def setup_columns(self):
        t = self.view['tree']
        t.set_model(self.model.tree_model)

        r = gtk.CellRendererText()
        c = gtk.TreeViewColumn('Name', r)
        c.set_cell_data_func(r, self.render)
        t.append_column(c)
    
    def render(self, column, cell, model, iter):
        cell.set_property("text", model[iter][0].name)

    def on_window_delete_event(self, window, event):
        gtk.main_quit()

    def on_button_clicked(self, button):
        self.model.doodle()

m = AddressBook()
m.add(Person("John"))
m.add(Person("Julia"))
m.add(Person("Aron"))
v = View()
c = Controller(m, v)

gtk.main()
