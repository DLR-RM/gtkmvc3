# PYGTKMVC Predicate contribution UI
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

import gobject
import gtk

class ComboBox(gtk.ComboBox):
    """
    Widgets use the changed signal unless noted otherwise and don't fire
    spuriously. get_symbol is None, not just False, until the value is useful.
    """

    def __init__(self, model=None):
        gtk.ComboBox.__init__(self, model)

        r = gtk.CellRendererText()
        self.pack_start(r, True)
        self.add_attribute(r, "text", 0)

        i = model.get_iter_first()
        if not model.iter_next(i):
            self.set_active_iter(i)

    def get_active_value(self, column):
        m = self.get_model()
        i = self.get_active_iter()
        if i:
            return m.get_value(i, column)

    def set_active_value(self, column, value):
        m = self.get_model()
        i = m.get_iter_first()
        while i:
            if m.get_value(i, column) == value:
                self.set_active_iter(i)
                break
            i = m.iter_next(i)

    def set_symbol(self, value):
        self.set_active_value(1, value)

    def get_symbol(self):
        return self.get_active_value(1)

    def get_factory(self):
        return self.get_active_value(2)

# ---------------------------------------------------------------
#        Right widgets
# ---------------------------------------------------------------

class Entry(gtk.Entry):

    def get_symbol(self):
        return self.get_text() or None

    def set_symbol(self, value):
        self.set_text(value)

class TagEntry(gtk.HBox):

    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, completion=None):
        gtk.HBox.__init__(self)

        e = gtk.Entry()
        e.set_properties(primary_icon_stock=gtk.STOCK_ADD,
            primary_icon_activatable=True, primary_icon_sensitive=True)
        e.connect("focus-out-event", self.on_input__focus_out)
        e.connect("activate", self.on_input__activate)
        e.connect("icon-release", self.on_input__icon_release)
        e.show()

        if completion:
            c = gtk.EntryCompletion()
            c.set_model(completion)
            c.set_text_column(0)
            c.connect("match-selected", self.on_completion__match_selected)
            e.set_completion(c)

        self.pack_end(e, expand=True)

    def on_completion__match_selected(self, completion, model, it):
        # Adding two tags this way and then deleting another crashes my GTK.
        self.add_tag(model.get_value(it, 0))
        completion.get_entry().set_text("")
        # Replace default handler as we can't seem to connect after it.
        return True

    def on_input__focus_out(self, entry, event):
        entry.set_text("")

    def on_input__icon_release(self, entry, position, event):
        self.on_input__activate(entry)

    def on_input__activate(self, entry):
        text = entry.get_text()
        if text:
            entry.set_text("")
            self.add_tag(text)

    def get_symbol(self):
        return tuple(e.get_text() for e in self.get_children()[:-1]) or None

    def set_symbol(self, tags):
        for e in self.get_children()[:-1]:
            self.remove(e)
        for t in tags:
            self.add_tag(t)

    def add_tag(self, text):
        e = gtk.Entry()
        e.set_properties(primary_icon_stock=gtk.STOCK_REMOVE,
            primary_icon_activatable=True, primary_icon_sensitive=True,
            editable=False, visible=True, text=text)
        self.fit_width(e)
        e.connect("icon-release", self.on_tag__icon_release)
        self.pack_start(e, expand=False)
        self.emit("changed")

    def fit_width(self, entry):
        # TODO set proportionaly more width for fewer characters.
        entry.set_properties(width_chars=len(entry.get_text()) + 2)

    def on_tag__icon_release(self, entry, position, event):
        self.remove(entry)
        self.emit("changed")

class SpinButton(gtk.SpinButton):

    def __init__(self):
        gtk.SpinButton.__init__(self, gtk.Adjustment(0, -9999, 9999, 1, 10))

    def get_symbol(self):
        return self.get_value_as_int()

    def set_symbol(self, value):
        self.set_value(value)

class Calendar(gtk.Calendar):

    def __init__(self):
        gtk.Calendar.__init__(self)

        self.set_properties(show_day_names=False)

    def get_symbol(self):
        y, m, d = self.get_date()
        return y, m + 1, d

    def set_symbol(self, value):
        self.freeze()
        self.select_month(value[1] - 1, value[0])
        self.select_day(value[2])
        self.thaw()

class Day(gtk.HBox):

    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self):
        gtk.HBox.__init__(self)

        self.calendar = gtk.Calendar()
        self.calendar.set_properties(show_day_names=False)
        self.calendar.connect("day-selected", self.on_calendar__changed)

        self.button = gtk.CheckButton("Today")
        self.button.connect("toggled", self.on_button__toggle)

        # TODO center, probably by using Alignment.
        self.pack_start(self.button)
        self.pack_start(self.calendar)
        self.show_all()

    def on_button__toggle(self, button):
        self.calendar.set_properties(sensitive=not button.get_active())
        self.emit("changed")

    def on_calendar__changed(self, widget):
        self.emit("changed")

    def get_symbol(self):
        if self.button.get_active():
            return "TODAY"
        y, m, d = self.calendar.get_date()
        return y, m + 1, d

    def set_symbol(self, value):
        date = value != "TODAY"
        self.button.set_active(not date)
        self.calendar.set_properties(sensitive=date)
        if date:
            self.calendar.freeze()
            self.calendar.select_month(value[1] - 1, value[0])
            self.calendar.select_day(value[2])
            self.calendar.thaw()

class CheckList(gtk.HBox):

    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, source):
        gtk.HBox.__init__(self)

        for display, symbol, _ in source:
            c = gtk.CheckButton(display)
            c.set_data("value", symbol)
            self.pack_start(c)
            c.connect("toggled", self.on_button__toggle)

        self.show_all()

    def on_button__toggle(self, button):
        self.emit("changed")

    def get_symbol(self):
        return tuple(c.get_data("value") for c in self.get_children()
            if c.get_active())

    def set_symbol(self, value):
        for c in self.get_children():
            c.set_active(c.get_data("value") in value)

class Label(gtk.Label):

    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def get_symbol(self):
        return ""

    def set_symbol(self, value):
        pass

# ---------------------------------------------------------------
#        Utility
# ---------------------------------------------------------------

def ListStore(*args):
    # Could use symbol object instead of str.
    s = gtk.ListStore(str, object, object)
    for row in args:
        s.append(row)
    return s

# ---------------------------------------------------------------
#        Internal
# ---------------------------------------------------------------

class Row(gtk.HBox):
    # TODO use gtk.Table instead.
    """
    Needs to be shown explicitly.
    """

    __gsignals__ = {
        "changed": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, left_factory):
        gtk.HBox.__init__(self)

        self._left = l = left_factory()
        l.connect("changed", self.on_left__changed)
        self.pack_start(l, False)

        self._operator = None
        self._operator_factory = None
        self._right = None
        self._right_factory = None

        self.add_button = a = gtk.Button()
        a.add(gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON))
        self.pack_end(a, False)

        self.remove_button = r = gtk.Button()
        r.add(gtk.image_new_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_BUTTON))
        self.pack_end(r, False)

        self._symbols = None

        self.on_left__changed(self._left)

    def emit_if_changed(self):
        new = self.get_symbols()
        if self._symbols != new:
            self._symbols = new
            self.emit("changed")

    def on_left__changed(self, widget):
        f = widget.get_factory()
        if self._operator_factory is not f:
            self._operator_factory = f
            if self._operator:
                self.remove(self._operator)
            if self._right:
                self.remove(self._right)
                self._right = None
                self._right_factory = None
            self._operator = o = f()
            self.pack_start(o, False)
            o.show()

            o.connect("changed", self.on_operator__changed)
            if o.get_factory():
                self.on_operator__changed(o)

        self.emit_if_changed()

    def on_operator__changed(self, widget):
        f = widget.get_factory()
        if self._right_factory is not f:
            self._right_factory = f
            if self._right:
                self.remove(self._right)
            self._right = o = f()
            self.pack_start(o, True)
            o.show()

            if isinstance(o, gtk.SpinButton):
                # Necessary to make typing work.
                o.connect("value-changed", self.on_right__changed)
            elif isinstance(o, gtk.Calendar):
                # Also fires for month/year.
                o.connect("day-selected", self.on_right__changed)
            else:
                o.connect("changed", self.on_right__changed)

        self.emit_if_changed()

    def on_right__changed(self, widget):
        self.emit_if_changed()

    def get_symbols(self):
        if self._right and self._right.get_symbol() is not None:
            return (self._left.get_symbol(), self._operator.get_symbol(),
                self._right.get_symbol())

    def set_symbols(self, value):
        self._left.set_symbol(value[0])
        self._operator.set_symbol(value[1])
        self._right.set_symbol(value[2])

# ---------------------------------------------------------------
#        Container widget
# ---------------------------------------------------------------

class Editor(gtk.VBox):
    __gproperties__ = {
        "symbols": (object, "nick", "desc", gobject.PARAM_READWRITE)
        }

    def __init__(self, left_factory):
        gtk.VBox.__init__(self)

        self._left_factory = left_factory

        self.add_new_row()

    def adjust_sensitive(self):
        c = self.get_children()
        c[0].remove_button.set_sensitive(len(c) > 1)

    def add_new_row(self, position=-1):
        r = Row(self._left_factory)
        r.connect("changed", self.on_row__changed)
        r.add_button.connect("clicked", self.on_add__clicked, r)
        r.remove_button.connect("clicked", self.on_remove__clicked, r)
        r.show_all()
        self.pack_start(r, False)
        self.reorder_child(r, position)
        self.adjust_sensitive()
        return r

    def on_row__changed(self, row):
        self.notify("symbols")

    def on_add__clicked(self, button, row):
        self.add_new_row(self.child_get_property(row, "position") + 1)

    def on_remove__clicked(self, button, row):
        self.remove(row)
        self.adjust_sensitive()
        if row.get_symbols():
            self.notify("symbols")

    def do_get_property(self, spec):
        if spec.name != "symbols":
            # Not sure this check is necessary.
            raise AttributeError
        value = []
        for r in self.get_children():
            v = r.get_symbols()
            if v:
                value.append(v)
        return value or None

    def do_set_property(self, spec, value):
        if spec.name != "symbols":
            raise AttributeError
        # Doesn't pay to reuse rows.
        for r in self.get_children():
            self.remove(r)
        # Apparently no freeze_notify necessary in do_set.
        for v in value:
            self.add_new_row().set_symbols(v)
