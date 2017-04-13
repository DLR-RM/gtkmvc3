# Author: Roberto Cavada, Copyright 2011
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
from gtkmvc import Controller
from gtkmvc.adapters import Adapter
import gtk


class MyCtrl (Controller):

    def register_view(self, view):
        view['window_top'].connect('delete-event', lambda w,e: gtk.main_quit())        
        view.setup_content(self.model.counter_names, self.model.get_max_value())
        return


    def register_adapters(self):
        for name in self.model.counter_names:
            self.adapt('counter_select', 'rb_'+name)
            pass
       
        self.adapt('counter_select', 'entry_select')        
        self.adapt('counter', 'label_counter')
        self.adapt('counter', 'adjustment_counter')

        # this is done to add some cosmetics to the label showing 'counter_select':
        adapter = Adapter(self.model, 'counter_select')
        adapter.connect_widget(
            self.view['label_select'],
            setter=lambda lbl, val: lbl.set_markup("Counter <b>%s</b>:" % val))
        self.adapt(adapter)        
        return


    # -------------------------------------------
    # Signals handling
    # -------------------------------------------
    def on_button_reset_clicked(self, b): self.model.reset()
    def on_button_incr_clicked(self, b): self.model.increment()

    
    # -------------------------------------------
    # Observable properties
    # -------------------------------------------
    @Controller.observe("counter", assign=True)
    def counter_notify(self, model, name, info):
        if model != self.model: return # not the model we want to observe

        if info.new == self.model.get_max_value(): self.view.show_red()            
        elif info.new == self.model.get_max_value() - 1: self.view.show_yellow()
        else: self.view.show_green()

        # button sensitivity
        self.view['button_incr'].set_sensitive(info.new != self.model.get_max_value())
        return

    pass # end of class
# ----------------------------------------------------------------------
