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


# In this example the model contains a date.
# A Calendar widget is connected to the model by an adapter.
# Pressing the button, the selected date is printed to the stdout.

import _importer
from gtkmvc import Model, Controller, View

import gtk


class MyView (View):
    glade = "adapters.glade"
    top = "window5"
    pass

import datetime
class MyModel (Model):
    data = datetime.datetime.today()
    __observables__ = ("data",)
    pass


class MyCtrl (Controller):

    def register_adapters(self):
        self.adapt("data", "calendar")
        return

    def on_button8_clicked(self, button): print self.model.data

    def on_window5_delete_event(self, w, e):
        gtk.main_quit()
        return True
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m,v)

gtk.main()



