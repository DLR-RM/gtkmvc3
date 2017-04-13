#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2006 by Roberto Cavada
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
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


import utils._importer
from gtkmvc import View

import utils.globals
import os.path
import gtk

class CurrencyView (View):
    """This is the view for the 'Currencies' dialog"""
    glade = os.path.join(utils.globals.GLADE_DIR, "currency.glade")
    top = "table_currency"

    def light_name(self, select):
        w = self['entry_name']
        w.grab_focus()
        if select: w.select_region(0, -1)
        return
    
    def set_name(self, name): self['entry_name'].set_text(name)
    def set_rate(self, rate): self['sb_rate'].set_value(rate)
    def set_notes(self, notes): self['tv_notes'].get_buffer().set_text(notes)

    def get_name(self): return self['entry_name'].get_text()
    def get_rate(self): return self['sb_rate'].get_value()
    def get_notes(self):
        buf = self['tv_notes'].get_buffer()
        return buf.get_text(*buf.get_bounds())
    
    pass # end of class
# ----------------------------------------------------------------------
