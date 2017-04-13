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
from yomanlib.utils.misc import get_buf_text

from gtkmvc import Controller
import gtk
import gobject

class AppCtl(Controller):
    def __init__(self, model, view):
        Controller.__init__(self, model, view, handlers='class')
        view.connect_signals(self)
        self.note = NoteCtrl(model.data.empty_note, view.note, self)
        self.main = MainCtrl(model.data, view.main, self.note)
        self.main.parent = self
        return

    def register_view(self, view):
        return

    def set_title(self, text):
        self.view['window_main'].set_title('Yoman: %s' % text)
        return
    
    def quit_application(self):
        gtk.main_quit()
        return

    def on_quit_activate(self, item):
        self.quit_application()
        return True

    def on_window_main_delete_event(self, window, event):
        self.quit_application()
        return True

    def on_about_activate(self, item):
        from yomanlib.views.appview import AppAboutView
        v = AppAboutView(parent_view=self.view)
        c = Controller(self.model, v, handlers='class')
        v.run()
        self.model.unregister_observer(c)
        return True

    def add_note(self):
        self.main.new_note(add_as_child=False)
        return
    
    def add_note_child(self):
        self.main.new_note(add_as_child=True)
        return

    def on_add_note_activate(self, item):
        self.add_note()
        return True

    def on_add_child_activate(self, item):
        self.add_note_child()
        return True

    def on_delete_note_activate(self, item):
        self.main.delete_selected()
        return True


class MainCtrl(Controller):
    def __init__(self, model, view, note_ctrl):
        Controller.__init__(self, model, view, handlers='class')
        view.connect_signals(self)
        self.note = note_ctrl
        return

    def register_view(self, view):
        treeview = self.view['treeview_main']
        treeselect = treeview.get_selection()
        treeselect.connect("changed", self.on_select_changed)
        treeview.set_model(self.model)
        return

    def get_selected(self):
        treeview = self.view['treeview_main']
        selection = treeview.get_selection()
        (model, parent) = selection.get_selected()
        return (selection, model, parent)

    def new_note(self, add_as_child):
        (selection, model, parent) = self.get_selected()
        if not add_as_child and parent is not None:
            # Adding as brother, find the parent of the current note
            parent = model.iter_parent(parent)
        iter = self.model.new_note(parent)

        # Set the new note as the selected one
        treeview = self.view['treeview_main']
        treeview.expand_to_path(self.model.get_path(iter))
        selection.select_iter(iter)
        self.note.take_focus(focus_title=True)
        return

    def delete_selected(self):
        (selection, model, cur_item) = self.get_selected()
        if cur_item is None:
            return
    
        path = self.model.get_path(cur_item)
        self.model.del_note(cur_item)

        # Try to select the item that replaced us in that location
        selection.select_path(path)
        # If nothing is selected, select the last item
        if not selection.path_is_selected(path):
            row = path[0]-1
            if row >= 0:
                selection.select_path((row,))
        return

    def on_select_changed(self, treeselect):
        (model, iter) = treeselect.get_selected()
        if iter is None:
            # Empty selection
            self.note.set_model(self.model.empty_note)
        else:
            # One element selected
            note = model.get_value(iter, self.model.OBJECT_INDEX)
            self.note.set_model(note)
        return True


class NoteCtrl(Controller):
    def __init__(self, model, view, window_ctrl):
        Controller.__init__(self, model, view, handlers='class')
        view.connect_signals(self)
        self.window_ctrl = window_ctrl
        self.stop_model_update = False
        return

    def register_view(self, view):
# Doesn't seem to be necessary and crashes GTK, except the old one on RHEL.
#       self.view['textview_note'].set_buffer(self.model)
        self.view['entry_title'].set_text(self.model.title)
        self.update_view()
        return

    def set_model(self, model):
        self.model.unregister_observer(self)
        self.model = model
        self.model.register_observer(self)

        if self.view is not None:
            self.view['textview_note'].set_buffer(model)
        self.update_view()
        return

    def take_focus(self, focus_title=False):
        if focus_title:
            widget = self.view['entry_title']
        else:
            widget = self.view['textview_note']
        widget.grab_focus()
        return

    def update_view(self):
        if self.view is None: return

        self.stop_model_update = True
        self.view['viewport_note'].set_sensitive(self.model.enabled)
        self.view['entry_title'].set_text(self.model.title)
        self.stop_model_update = False
        return


    def on_entry_title_changed(self, entry):
        if self.stop_model_update:
            return True
        self.model.title = entry.get_text()
        return True

    # ----------------------------------------
    # Observable properties
    # ----------------------------------------

    @Controller.observe("title", assign=True)
    @Controller.observe("enabled", assign=True)
    def enabled_value_change(self, model, prop_name, info):
        self.update_view()
        if prop_name == "title": self.window_ctrl.set_title(info.new)
        return
    
    pass
