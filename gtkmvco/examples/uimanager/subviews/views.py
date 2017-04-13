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


from gtkmvc import View
import gtk


class ApplView (View):
    builder = "ui/appl.glade"
    top = "window_appl"

    def __init__(self):
        View.__init__(self)

        # creates sub views:
        self.part1 = Part1View()
        self.part2 = Part2View()
        self.part3 = Part3View()
        self.bars = BarsView(self) # this has to be the last
        
        # connects sub views:
        self['vbox_top'].pack_start(self.bars.get_top_widget())
        self['algn_part1'].add(self.part1.get_top_widget())
        self['algn_part2'].add(self.part2.get_top_widget())
        self['algn_part3'].add(self.part3.get_top_widget())
        return
    
    pass  # end of class
# --------------------------------------------------------------------


class BarsView (View):
    builder = "ui/bars.glade"
    top = "vbox_bars"

    def __init__(self, appl_view):
        View.__init__(self)

        self.get_top_widget().unparent()
        self['window1'] = None  # gets rid of the containing window
        
        # uim and accel group
        self.ui = gtk.UIManager()
        acc_grp = self.ui.get_accel_group()
        appl_view.get_top_widget().add_accel_group(acc_grp)

        # add action groups
        for view, agrp in [(self, "agrp_bars"),
                           (appl_view, "agrp_appl"),
                           (appl_view.part1, "agrp_part1"),
                           (appl_view.part2, "agrp_part2"),
                           (appl_view.part3, "agrp_part3"),]:
            self.ui.insert_action_group(view[agrp])
            pass

        # Connects all accelerators declared in glade.  This is
        # needed as action created in glade are connected to the
        # top-level window acceleration group, and that window is
        # not used here. Only the application Windows is used, and
        # in fact the agrp_appl is not needed to be connected here.
        for view, agrp in [(self, "agrp_bars"),
                           (appl_view.part1, "agrp_part1"),
                           (appl_view.part2, "agrp_part2"),
                           (appl_view.part3, "agrp_part3"),]:
            for action in view[agrp].list_actions():
                action.set_accel_group(acc_grp)
                action.connect_accelerator()
                pass
            pass

        self.ui.add_ui_from_file("ui/ui.xml")
        for name in "MainMenuBar MainToolBar".split():
            widget = self.ui.get_widget('/' + name)
            assert widget
            self[name] = widget
            self['vbox_bars'].pack_start(widget, expand=False)
            pass

        return
    pass  # end of class
# --------------------------------------------------------------------


class Part1View (View):
    builder = "ui/part1.glade"
    top = "vbox_top"

    def __init__(self):
        View.__init__(self)

        self.get_top_widget().unparent()
        self['window1'] = None  # gets rid of the containing window
        return
    pass  # end of class
# --------------------------------------------------------------------


class Part2View (View):
    builder = "ui/part2.glade"
    top = "hbox_top"

    def __init__(self):
        View.__init__(self)

        self.get_top_widget().unparent()
        self['window1'] = None  # gets rid of the containing window

        # custom toolitems
        from spintool import SpinToolAction
        act = SpinToolAction("action_part2_sb_counter",
                             "Counter", "Counter of Part2!",
                             "Counter:",
                             self['sb_count'].get_adjustment())
        self['action_part2_sb_counter'] = act
        agrp = self['agrp_part2']
        agrp.add_action(act)
        return
    pass  # end of class
# --------------------------------------------------------------------


class Part3View (View):
    builder = "ui/part3.glade"
    top = "vbox_top"

    def __init__(self):
        View.__init__(self)

        self.get_top_widget().unparent()
        self['window1'] = None  # gets rid of the containing window
        return
    pass  # end of class
# --------------------------------------------------------------------

