# Author: Roberto Cavada, Copyright 2004
#
# This is free software; you can redistribute it and/or 
# modify it under the terms of the GNU Lesser General Public 
# License as published by the Free Software Foundation; either 
# version 2 of the License, or (at your option) any later version.
#
# These examples are distributed in the hope that they will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# Lesser General Public License for more details.

import _importer
from gtkmvc import View


# ----------------------------------------------------------------------
class MyView (View):
    """Glade-based view class.

       The view is a window containing a button and a label. The
       label shows the value of a counter contained in the
       model. Of course the controller wil provide the
       connection. Every time the button is pressed, the counter
       will be incremented."""
    glade = "pygtkmvc-example.glade"

    def set_text(self, text):
        self['label'].set_text(text)
        return

    pass # end of class
# ----------------------------------------------------------------------
