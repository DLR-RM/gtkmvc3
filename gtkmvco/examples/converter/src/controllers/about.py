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
from gtkmvc import Controller
import gtk
import gobject

class AboutCtrl (Controller):
    """Controller of 'About' dialog. It handles the scrolling of the
    credits label, and the close button.""" 

    def register_view(self, view):
        """Loads the text taking it from the model, then starts a
        timer to scroll it."""
        self.view.set_text(self.model.credits)
        gobject.timeout_add(1500, self.on_begin_scroll)
        return


    # ---------------------------------------------------
    #                  user callbacks
    # ---------------------------------------------------
    def on_begin_scroll(self):
        """Called once after 2.1 seconds"""
        gobject.timeout_add(50, self.on_scroll)
        return False 

    def on_scroll(self):
        """Called to scroll text"""
        try:
            sw = self.view['sw_scroller']
        except KeyError:
            return False # destroyed!        
        vadj = sw.get_vadjustment()
        if vadj is None: return False
        val = vadj.get_value()
        
        # is scrolling over?
        if val >= vadj.upper - vadj.page_size:
            self.view.show_vscrollbar()
            return False
        
        vadj.set_value(val+0.5)
        return True
    
    
    # ---------------------------------------------------
    #                    gtk signals
    # ---------------------------------------------------
    #def on_dialog_about_delete_event(self, win, event):
    #    return True

    #def on_button_close_clicked(self, button):
    #    return

    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    @Controller.observe("credits", assign=True)
    def credits_change(self, m, n, info):
        self.view.set_text(info.new)
        return

    pass # end of class


