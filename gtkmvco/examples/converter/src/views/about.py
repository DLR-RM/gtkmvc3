#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


import utils._importer
from gtkmvc3 import View

import utils.globals
import os.path
import gtk

class AboutView (View):
    """This is the view for the 'About' dialog"""
    
    glade = os.path.join(utils.globals.GLADE_DIR, "about.glade") 

    def set_text(self, text):
        self['label_text'].set_markup(text)
        return

    def run(self):
        res = self['dialog_about'].run()
        self['dialog_about'].destroy()
        return res
    
    def show_vscrollbar(self, show=True):
        sw = self['sw_scroller']
        hpol, vpol = sw.get_policy()
        if show: vpol = gtk.POLICY_ALWAYS
        else: vpol = gtk.POLICY_NEVER
        sw.set_policy(hpol, vpol)
        return
    
    pass # end of class
# ----------------------------------------------------------------------
