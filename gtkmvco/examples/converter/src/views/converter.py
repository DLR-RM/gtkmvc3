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
import utils.globals
from amount import AmountView

from gtkmvc import View

import os.path


# ----------------------------------------------------------------------
class ConverterView (View):
    """A view for the converter"""
    
    glade = os.path.join(utils.globals.GLADE_DIR, "converter.glade")

    def __init__(self, stand_alone=True):
        """stand_alone means that this view has a its-own windows, i.e. the
        converter is used as a stand alone (non embedded) application"""

        if stand_alone: twid = "window_converter"
        else: twid = "vbox_converter"
        View.__init__(self, top=twid)

        # creates and connects sub views
        self.source = AmountView()
        self.target = AmountView()

        self.setup_widgets()

        # makes target uneditable
        self.target.set_editable(False)

        return

    def setup_widgets(self):
        vbox = self['vbox_converter']
        wid = self.source.get_top_widget()
        vbox.pack_start(wid)
        vbox.reorder_child(wid, 0)
        
        wid = self.target.get_top_widget()
        vbox.pack_end(wid)
        return

    def is_stand_alone(self):
        try:
            return self["window_converter"] is not None
        except KeyError:
            return True

    pass # end of class
# ----------------------------------------------------------------------
