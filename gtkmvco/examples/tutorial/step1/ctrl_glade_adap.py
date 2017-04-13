# Author: Roberto Cavada, Copyright 2007
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



# This is file ctrl_glade_adapt.py
import _importer
from gtkmvc import Controller
import gtk

class MyControllerAdap (Controller):

    def register_view(self, view):
        """This method is called by the view, that calls it when it
        is ready to register itself. Here we connect the 'pressed'
        signal of the button with a controller's method. Signal
        'destroy' for the main window is handled as well."""

        # connects the signals:
        self.view['main_window'].connect('destroy', gtk.main_quit)        
        return

    def register_adapters(self):
        # This is a simple adapter
        #self.adapt("counter", "label")

        # This is for a custom adapter
        from gtkmvc import adapters
        a = adapters.Adapter(self.model, "counter")
        a.connect_widget(self.view['label'], 
                         setter=lambda w,v: 
                         w.set_markup("<big>counter=<b>%02d</b></big>" % v))
        self.adapt(a)
        return
       
    # signals:
    def on_button_clicked(self, button):
        self.model.counter += 1  # changes the model
        return
    
    pass # end of class
