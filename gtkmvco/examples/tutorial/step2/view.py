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
from gtkmvc import View
import gtk

class MyView (View):
    builder = "glade/tut_step2.glade"
    top = "window_top"

    def __init__(self):
        View.__init__(self)

        self.red_pb = gtk.gdk.pixbuf_new_from_file("img/red.png")
        self.yellow_pb = gtk.gdk.pixbuf_new_from_file("img/yellow.png")
        self.green_pb = gtk.gdk.pixbuf_new_from_file("img/green.png")

        self.show_green()        
        return


    def setup_content(self, names, max_value):
        """Creates the radio buttons for counter selection, and sets
        up the progress bar.
        
        @param names is an iterable of strings for the names of counters.
        @param max_value is the maximum value used to set the progress bar.

        This method is called by controllers, when connected model is
        available.
        """

        # radio buttons
        box = self['vbox_rb']
        group = None        
        for name in names:
            if 'rb_'+name in self: continue # skip already created names
            
            rb = gtk.RadioButton(group, name)
            self['rb_'+name] = rb
            rb.set_visible(True)
            box.pack_start(rb, expand=False)
            group = group or rb
            pass

        # progress bar:
        self['adjustment_counter'].set_upper(max_value)
        return


    # these set the image
    def show_red(self): self['image'].set_from_pixbuf(self.red_pb)
    def show_yellow(self): self['image'].set_from_pixbuf(self.yellow_pb)
    def show_green(self): self['image'].set_from_pixbuf(self.green_pb)        

    pass # end of class
# ----------------------------------------------------------------------
