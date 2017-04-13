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

from currency import CurrencyView

import utils.globals
import os.path
import gtk

# ----------------------------------------------------------------------
class CurrenciesView (View):
    """This is the view for the 'Currencies' dialog"""
    glade = os.path.join(utils.globals.GLADE_DIR, "currencies.glade")
    top = "dialog_currencies"

    def add_currency_view(self, select=False):
        """returns the newly added view"""
        v = CurrencyView()
        self.remove_currency_view()
        self['hbox_top'].pack_end(v.get_top_widget())
        v.light_name(select)
        return v

    def remove_currency_view(self):
        hbox = self['hbox_top']
        ch = hbox.get_children()
        if len(ch) > 1: hbox.remove(ch[-1])
        return

    def destroy(self):
        self['dialog_currencies'].destroy()
        return
    
    pass # end of class
# ----------------------------------------------------------------------
