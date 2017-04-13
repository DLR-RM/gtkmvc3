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

from ctrl_glade import MyController

class MyControllerNoGlade (MyController):
    """Customized controller. 

    The controller carries out two tasks:
       - When view's button is clicked, increments model property
         'counter'
       - When the property changes, updates the view's label text
         correspondently. This means that the controller is
         an observer for property 'counter' as well."""

    def register_view(self, view):
        # connects the signals:
        self.view['button'].connect('clicked', self.on_button_clicked)
        return    
    
    pass # end of class
# ----------------------------------------------------------------------

