#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2012 by Roberto Cavada
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
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


from gtkmvc import Controller
from gtkmvc.adapters import Adapter
from spintool import SpinToolAction
import gtk
import gobject


class ApplCtrl (Controller):

    def __init__(self, m, v):
        Controller.__init__(self, m, v)

        # creates sub controllers
        self.bars = BarsCtrl(m, v.bars, self)
        self.part1 = Part1Ctrl(m.part1, v.part1)
        self.part2 = Part2Ctrl(m.part2, v.part2)
        self.part3 = Part3Ctrl(m.part3, v.part3)
        return

    # ---------------------
    # signal handlers
    # ---------------------
    def on_action_file_quit_activate(self, what):
        gtk.main_quit()
        return
    
    def on_window_appl_delete_event(self, w, e):
        self.view['action_file_quit'].activate()
        return False
    
    pass  # end of class
# --------------------------------------------------------------------


class BarsCtrl (Controller):
    def __init__(self, m, v, appl_ctrl):
        Controller.__init__(self, m, v)
        return
    
    pass  # end of class
# --------------------------------------------------------------------


class Part1Ctrl (Controller):

    def register_view(self, view):
        view['tv_msg'].set_buffer(self.model.buf)
        return

    def register_adapters(self):
        self.adapt("lines")
        return
    
    # ---------------------
    # signal handlers
    # ---------------------
    def on_action_part1_insert_activate(self, what):
        self.model.insert()
        return

    def on_action_part1_clear_activate(self, what):
        self.model.clear()
        return
    
    pass  # end of class
# --------------------------------------------------------------------


class Part2Ctrl (Controller):
    def register_adapters(self):
        # The Action for the spinbutton is adapted here manually:
        sb_adapter = Adapter(self.model, "counter")
        sb_adapter.connect_widget(self.view['action_part2_sb_counter'],
                                  SpinToolAction.get_value,
                                  SpinToolAction.set_value,
                                  "changed")
        self.adapt(sb_adapter)

        # here the other spinbutton is adapted
        self.adapt("counter", "sb_count")
        return

    pass  # end of class
# --------------------------------------------------------------------


class Part3Ctrl (Controller):

    def register_adapters(self):
        self.adapt("running", "action_part3_run")
        return

    # ---------------------
    # signal handlers
    # ---------------------
    def _pb_tick(self):
        self.view['pbar'].pulse()
        return self.model.running
        
    # ---------------------
    # notifications
    # ---------------------
    @Controller.observe("running", assign=True)
    def notify_running(self, model, name, info):
        # starts/stops the progressbar
        if info.new:
            # notice that we may start multiple timers, if 'running'
            # is toggled on faster than pulse interval. For this
            # example we do not mind at all... 
            gobject.timeout_add(250, self._pb_tick)
        return

    pass  # end of class
# --------------------------------------------------------------------
