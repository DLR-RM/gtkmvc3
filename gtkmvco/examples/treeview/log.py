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
Usage:

cd /interesting/directory
svn log --xml > report
python log.py report
"""

import datetime
import sys
import xml.etree.cElementTree as ElementTree

import gtk

import _importer
import gtkmvc

import editor
import filtering
import predicates

class Entry(object):
    def __init__(self, node):
        self.revision = int(node.attrib['revision'])
        # TODO handle timezone.
        self.date = datetime.datetime.strptime(node.findtext('date'),
            '%Y-%m-%dT%H:%M:%S.%fZ')
        self.author = node.findtext('author')
        self.message = node.findtext('msg')

    @property
    def day(self):
        # TODO replace with predicate that can compare (y, m, d) to datetime.
        return self.date.year, self.date.month, self.date.day

def EntryStore(path):
    store = gtk.ListStore(object)
    tree = ElementTree.parse(path)
    for child in tree.getroot().getchildren():
        store.append([Entry(child)])
    return store

def Editor():
    NUMBER = editor.ListStore(
        ("is smaller than", 'lt', editor.SpinButton),
        ("is greater than", 'gt', editor.SpinButton),
        )
    Number = lambda: editor.ComboBox(NUMBER)

    STRING = editor.ListStore(
        ("contains", 'contains', editor.Entry),
        )
    String = lambda: editor.ComboBox(STRING)

    DATE = editor.ListStore(
        ("after", 'gt', editor.Calendar),
        ("before", 'lt', editor.Calendar),
        )
    Date = lambda: editor.ComboBox(DATE)

    FIELD = editor.ListStore(
        ("Date", 'day', Date),
        ("Revision", 'revision', Number),
        ("Author", 'author', String),
        )
    Field = lambda: editor.ComboBox(FIELD)

    return editor.Editor(Field)

class View(gtkmvc.View):
    def __init__(self):
        gtkmvc.View.__init__(self, builder="log.ui", top="window")

        t = self['treeview']
        # Make GtkTreeSelection available to signal connection via method
        # name pattern.
        # Some version of GTK 3 and some version of Glade allowed it to be
        # named in the XML. Before it need not even have get_name(). See
        # https://bugzilla.gnome.org/show_bug.cgi?id=383766
        # and its (not marked as such) duplicate
        # https://bugzilla.gnome.org/show_bug.cgi?id=622735
        self['selection'] = t.get_selection()
        self['buffer'] = self['textview'].get_buffer()

        c = gtk.TreeViewColumn("Revision", gtk.CellRendererText())
        c.set_name('revision')
        t.append_column(c)

        c = self['date'] = gtk.TreeViewColumn("Date", gtk.CellRendererText())
        c.set_name('date')
        t.append_column(c)

        c = gtk.TreeViewColumn("Author", gtk.CellRendererText())
        c.set_name('author')
        t.append_column(c)

        e = self['editor'] = Editor()
        self['vbox'].pack_start(e)
        self['vbox'].reorder_child(e, 0)

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view.show()

    def register_adapters(self):
        self.setup_columns()
        # Overwrite one to improve formatting.
        gtkmvc.controller.setup_column(
            self.view['date'], attribute='date',
            from_python=lambda d: d.strftime('%Y.%m.%d %H:%M'))

        m = EntryStore(sys.argv[1]).filter_new()
        self.view['treeview'].set_model(m)
        self.visible_func = filtering.get_visible_function(m)

        # TODO way to write :: in magic handler method names.
        self.view['editor'].connect('notify::symbols', self.on_editor_changed)

    def on_editor_changed(self, widget, spec):
        symbols = widget.get_property('symbols')
        if not symbols:
            # TODO avoid None?
            symbols = ()
        self.visible_func.refilter(symbols, predicates)

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

    def on_selection__changed(self, widget):
        store, iter_ = widget.get_selected()
        if iter_:
            # Encode to UTF-8?
            self.view['buffer'].set_text(store[iter_][0].message)
        else:
            self.view['buffer'].set_text('')

c = Controller(gtkmvc.Model(), View(), handlers='class')
gtk.main()
