##  ===========================================================================
##  This file is part of Yoman, a notebook program.
##
##  Author: Baruch Even <baruch@ev-en.org>
##
##  Copyright (c) 2006 by Baruch Even
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program; if not, write to the Free Software Foundation, Inc.,
##  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##  The author may be contact at his email <baruch@ev-en.org>.
##
##  ===========================================================================


from yomanlib.utils import _importer
from yomanlib.utils import globals

from view import *
import gtk, gobject
import os

GLADE_FILE = 'glade/yoman.glade'

class AppView(Window):

	def __init__(self):
		Window.__init__(self, GLADE_FILE, 'window_main', "actiongroup1")

		self.main = MainView()
		self.note = NoteView()

		self.main.reparent(self, 'scrolledwindow_main')
		self.note.reparent(self, 'scrolledwindow_note')
		self.add_ui_from_file('glade/menu.xml')
		self["vbox1"].pack_start(self["/menubar"], expand=False)
		self["vbox1"].reorder_child(self["/menubar"], 0)
		return
        

class MainView(Widget):
	def __init__(self):
		Widget.__init__(self, GLADE_FILE, 'treeview_main')
		treeview = self.get_toplevel()
		treeview.set_reorderable(True)
		cell = gtk.CellRendererText()
		tvcolumn = gtk.TreeViewColumn('Title', cell, text=0)
		treeview.append_column(tvcolumn)

class NoteView(Widget):

	def __init__(self):
		Widget.__init__(self, GLADE_FILE, 'viewport_note')
		self['textview_note'].set_wrap_mode(gtk.WRAP_WORD)

class AppAboutView(Window):
	TOP_WIDGET = 'aboutdialog'

	def __init__(self, parent_view):
		Window.__init__(self, GLADE_FILE, 'aboutdialog')
		self.set_transient_for(parent_view)

	def run(self):
		f = open(os.path.join(globals.TOPDIR, "LICENSE"), "r")
		self['aboutdialog'].set_license(f.read())
		f.close()

		w = self.get_toplevel()
		res = w.run()
		w.destroy()
		return res
