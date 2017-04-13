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

import gtk
import gobject

# The code for creating custom action is inspired to project Gramps,
# which you can see here:
#  http://gramps.sourcearchive.com/documentation/3.3.1-1/valueaction_8py_source.html


class SpinToolItem (gtk.ToolItem):
    """This class is a ToolItem featuring a SpinButton with an
    optional Label"""

    __gtype_name__ = "SpinToolItem"

    __gsignals__ = {
        'changed': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE, #return value
                    ()), # arguments
    }

    def __init__(self, label=None, adj=None):
        gtk.ToolItem.__init__(self)

        self.set_border_width(2)
        hbox = gtk.HBox()
        self.sb = gtk.SpinButton(adj)
        if label:
            self.label = gtk.Label(label)
            hbox.pack_start(self.label)
            pass
        hbox.pack_start(self.sb)
        hbox.show_all()

        self.add(hbox)
        self.set_is_important(True)

        self.sb.connect("change-value", self._on_sb_changed)
        return

    def _on_sb_changed(self, sb):
        self.emit('changed')
        return

    def set_value(self, val):
        self.sb.set_value(val)

    def get_value(self):
        return self.sb.get_value()
    
    pass  # end of class
# --------------------------------------------------------------------


class SpinToolAction(gtk.Action):
    """An Action which handle a SpinToolItem instance"""

    __gtype_name__ = "SpinToolAction"

    __gsignals__ = {
        'changed': (gobject.SIGNAL_RUN_FIRST, 
                    gobject.TYPE_NONE, #return value
                    ()), # arguments
                    }

    def __init__(self, name, label, tooltip, *args):
        """Create a new SpinToolAction instance.

        @param args: arguments to be passed to the SpinToolItem
        class constructor.
        @type args: list
        """
        gtk.Action.__init__(self, name, label, tooltip, None)

        self._value = 0
        self._args_for_toolitem = args
        self._changed_handlers = {}

        self.set_tool_item_type(SpinToolItem)
        return

    def _on_proxy_changed(self, proxy):
        self.set_value(proxy.get_value())
        return

    def do_create_tool_item(self):
        """This is called by the UIManager when it is time to
        instantiate the proxy"""
        proxy = SpinToolItem(*self._args_for_toolitem)
        self.connect_proxy(proxy)
        return proxy

    def connect_proxy(self, proxy):
        if not isinstance(proxy, SpinToolItem):
            raise TypeError

        proxy.set_value(self._value)
        self._changed_handlers[proxy] = \
            proxy.connect('changed',
                          self._on_proxy_changed)

        # NOTE: it seems that Action.connect_proxy is not overridden
        # by this method
        return

    def set_value(self, value):
        """Set value to action."""
        self._value = value

        for proxy in self.get_proxies():
            proxy.handler_block(self._changed_handlers[proxy])
            proxy.set_value(self._value)
            proxy.handler_unblock(self._changed_handlers[proxy])
            pass

        self.emit('changed')
        return

    def get_value(self):
        """Set value to action."""
        return self._value

    pass  # end of class
