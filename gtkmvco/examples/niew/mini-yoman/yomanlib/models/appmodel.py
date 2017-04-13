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

from gtkmvc import Model, TreeStoreModel, TextBufferModel

import gtk
import gobject
import os

def recursive_find(self, index, obj):
    def do_recursive_find(self, index, obj, iter):
        while iter:
            # Match the current node
            if self.get_value(iter, index) == obj:
                return iter
            # Try to match any children nodes
            child_iter = self.iter_children(iter)
            if child_iter is not None:
                res = do_recursive_find(self, index, obj, child_iter)
                if res is not None:
                    return res
            # The current and its children are no match, continue
            iter = self.iter_next(iter)
        return None
    iter = self.get_iter_first()
    return do_recursive_find(self, index, obj, iter)


class AppModel(Model):

    def __init__(self):
        Model.__init__(self)
        self.data = DataModel()
        self.clear()

    def clear(self):
        self.data.clear()

    pass


class NoteModel(TextBufferModel):
    enabled = True
    title = ""
    __observables__ = ("enabled", "title")

    def __init__(self, title="", text="", enabled=True):
        TextBufferModel.__init__(self)
        self.enabled = enabled
        self.title = title
        self.set_text(text)
    
    pass

class DataModel(TreeStoreModel):

    TITLE_INDEX = 0
    OBJECT_INDEX = 1

    def __init__(self):
        TreeStoreModel.__init__(self, gobject.TYPE_STRING,
                                      gobject.TYPE_PYOBJECT)

        self.clear()
        pass

    def new_note(self, parent=None):
        note = NoteModel(title="New Note")
        return self.add_note(note, parent)

    def add_note(self, note, parent=None):
        note.register_observer(self)
        iter = self.append(parent, (note.title, note))
        return iter

    def del_note(self, note_iter):
        if note_iter is None:
            return
        note = self.get_value(note_iter, self.OBJECT_INDEX)
        note.unregister_observer(self)
        self.remove(note_iter)

    def clear(self):
        self.empty_note = NoteModel(enabled=False)
        TreeStoreModel.clear(self)
        return

    @Model.observe("title", assign=True)
    def title_value_change(self, model, _, info):
        iter = recursive_find(self, self.OBJECT_INDEX, model)
        assert(iter is not None)
        self.set_value(iter, self.TITLE_INDEX, model.title)
        return
    
    pass
