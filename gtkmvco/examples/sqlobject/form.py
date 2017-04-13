# PYGTKMVC Lazy text field
# Copyright (C) 2010  Tobias Weber
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
Demonstrating an adapter that don't updates the model for every character
typed but only when necessary. Useful to minimize database traffic.
"""

import _importer

import gtkmvc
from gtkmvc.support.utils import cast_value

class EntryController(gtkmvc.Observer):
    def __init__(self, widget, property, model=None):
        """
        *widget* a `gtk.Entry` instance.

        *property* a string (may not contain dots)

        *model* optionally call `set_model` with this.
        """
        gtkmvc.Observer.__init__(self)

        self.busy = False

        self.widget = widget
        widget.connect('activate', self.widget_notification)
        widget.connect('focus-out-event', self.widget_notification)

        self.property = property
        self.observe(self.model_notification, property, assign=True)

        self.model = None
        self.set_model(model)

    def get_property(self):
        return getattr(self.model, self.property) if self.model else None

    def set_property(self, new):
        if self.model:
            old = getattr(self.model, self.property)
            if old is not None:
                new = cast_value(new, type(old))
            setattr(self.model, self.property, new)

    def get_widget(self):
        return self.widget.get_text()

    def set_widget(self, new):
        self.widget.set_text('' if new is None else unicode(new))

    def widget_notification(self, *args):
        if not self.busy:
            self.busy = True
            self.set_property(self.get_widget())
            self.busy = False

    def model_notification(self, *args):
        if not self.busy:
            self.busy = True
            self.set_widget(self.get_property())
            self.busy = False            

    def set_model(self, model):
        """
        *model* a `Model` instance, or None.
        """
        if self.model:
            self.model.unregister_observer(self)
        self.model = model
        if self.model:
            self.model.register_observer(self)
            self.model_notification()
        else:
            self.set_widget(None)
        self.widget.set_sensitive(bool(self.model))

from gtkmvc.adapters import Adapter

import gtk

class Model(gtkmvc.Model):
    __observables__ = ['text']
    text = ''

class Controller(gtkmvc.Controller):
    def register_adapters(self):
        self.a = Model()
        self.b = Model()
        self.c = EntryController(self.view['e'], 'text')

        Adapter(self.a, 'text').connect_widget(self.view['a'])
        Adapter(self.b, 'text').connect_widget(self.view['b'])

    def on_button_a__clicked(self, widget):
        self.c.set_model(self.a)

    def on_button_b__clicked(self, widget):
        self.c.set_model(self.b)

    def on_button_none__clicked(self, widget):
        self.c.set_model(None)

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

if __name__ == '__main__':
    c = Controller(gtkmvc.Model(), gtkmvc.View(builder="form.ui"),
        handlers='class')
    gtk.main()
