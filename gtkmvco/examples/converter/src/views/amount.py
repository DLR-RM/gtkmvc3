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

# ----------------------------------------------------------------------
class AmountView (View):
    """A view for a single amount"""
    
    glade = os.path.join(utils.globals.GLADE_DIR, "amount.glade")
    top = "table_top"

    def set_editable(self, flag):
        sb = self['sb_amount']
        sb.set_editable(flag)
        sb.set_increments(0,0)
        return

    pass # end of class
# ----------------------------------------------------------------------
