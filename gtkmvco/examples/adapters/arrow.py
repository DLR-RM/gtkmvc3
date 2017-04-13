#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2008 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#  02111-1307 USA.
#
#  For more information on pygtkmvc see
#  <http://pygtkmvc.sourceforge.net> or email to the author Roberto
#  Cavada <roboogle@gmail.com>.  Please report bugs to
#  <roboogle@gmail.com>.


import _importer
from gtkmvc import Model, Controller, View

import gtk

# In this example the model contains the direction of an arrow.
# An arrow widget is connected to reflect that value that can be
# changed by pressing a button

class MyView (View):
    def __init__(self):
        View.__init__(self, "adapters.glade", "window8")
        return
    pass


class MyModel (Model):
    dir = gtk.ARROW_UP
    __observables__ = ("dir",)
    pass


class MyCtrl (Controller):

    def register_adapters(self):
        self.adapt("dir")
        return

    def on_button5_clicked(self, button):
        vals = [gtk.ARROW_UP, gtk.ARROW_RIGHT, gtk.ARROW_DOWN, gtk.ARROW_LEFT]
        self.model.dir = vals[(vals.index(self.model.dir)+1) % len(vals)]
        return

    def on_window8_delete_event(self, w, e):
        gtk.main_quit()
        return True
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()



