# PYGTKMVC View Component
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

class _Abstract(object):
    def __init__(self, arg, *args, **kwargs):
        self.builder = gtk.Builder()
        if "domain" in kwargs:
            self.builder.set_translation_domain(kwargs["domain"])
        self.items = {}
        if isinstance(arg, gtk.Widget):
            self.items[args[0]] = arg
            args = ()
            if args or kwargs:
                raise ValueError
            self.toplevel = arg
        else:
            self.builder.add_objects_from_file(arg, args)
            self.toplevel = self.builder.get_object(args[0])
        self.manager = gtk.UIManager()
        if isinstance(self.toplevel, gtk.Window):
            self.toplevel.add_accel_group(self.manager.get_accel_group())
        # Make Adjustment accessible
        for name in args:
            # Allow for ActionGroup detection
            self[name] = self.builder.get_object(name)
        # Cache
        for widget in self.builder.get_objects():
            try:
                name = gtk.Buildable.get_name(widget)
            except TypeError:
                pass
            else:
                self[name] = widget
        self.connected = False

    def __getitem__(self, name):
        """
        Also accepts widget paths for the internal UIManager. To get Actions
        you must use their name, not their path.
        """
        if name[0] == "/":
            return self.manager.get_widget(name)
        return self.items[name]

    def __setitem__(self, name, widget):
        if (isinstance(widget, gtk.ActionGroup) and
            widget not in self.manager.get_action_groups()):
            self.manager.insert_action_group(widget)
        self.items[name] = widget

    def __iter__(self):
        return iter(self.items)

    def connect_signals(self, target):
        """
        This is deprecated. Pass your controller to connect signals the old
        way.
        """
        if self.connected:
            raise RuntimeError("GtkBuilder can only connect signals once")
        self.builder.connect_signals(target)
        self.connected = True

    def get_toplevel(self):
        return self.toplevel

class Widget(_Abstract):
    def __init__(self, arg, *args, **kwargs):
        """
        When creating widgets in code, pass two arguments: a
        :class:`gtk.Widget` instance and a string naming it.

        To use GtkBuilder you pass the path to the XML file and between one
        and many names of widgets you'd like to load, e.g. "box1",
        "liststore1". The first will become our :meth:`get_toplevel`.
        """
        _Abstract.__init__(self, arg, *args, **kwargs)
        if self.toplevel.flags() & gtk.TOPLEVEL:
            raise TypeError

    def reparent(self, other, name):
        """
        Remove :meth:`get_toplevel` from any current parent and add it to
        *other[name]*.
        """
        # http://developer.gnome.org/gtk-faq/stable/x635.html
        # warns against reparent()
        old = self.toplevel.get_parent()
        if old:
            old.remove(self.toplevel)
        new = other[name]
        new.add(self.toplevel)

class Window(_Abstract):
    def __init__(self, arg, *args, **kwargs):
        """
        Works just like :class:`Widget`.

        Using GtkBuilder you can load more than one window into an instance,
        but this makes re-using your views harder and may be removed in the
        future.

        The limitations of these classes reflect best practices. If you don't
        like them write your view from scratch. As long as you use
        handler="class" all the controller expects is __getitem__ and
        __iter__.
        """
        _Abstract.__init__(self, arg, *args, **kwargs)
        if not self.toplevel.flags() & gtk.TOPLEVEL:
            raise TypeError

    def add_ui_from_file(self, path):
        """
        When you add ActionGroups through Glade or :meth:`__setitem__` they
        are automatically inserted into an internal UIManager. Its
        accelerators are set up with our toplevel window. All you have to do
        is use this method to load some XML and pack the widgets.
        """
        self.manager.add_ui_from_file(path)

    def set_transient_for(self, other):
        """
        *other* a :class:`Window` instance.
        """
        self.toplevel.set_transient_for(other.get_toplevel())

    def show(self):
        self.toplevel.show_all()

    def hide(self):
        self.toplevel.hide_all()
