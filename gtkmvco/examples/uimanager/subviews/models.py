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

from gtkmvc import Model
import gtk


class ApplModel (Model):

    def __init__(self):
        Model.__init__(self)

        # creates sub models
        self.part1 = Part1Model()
        self.part2 = Part2Model()
        self.part3 = Part3Model()
        
        return

    pass  # end of class
# --------------------------------------------------------------------


class Part1Model (Model):
    lines = 0
    __observables__ = ("lines",)
    
    def __init__(self):
        Model.__init__(self)

        self.buf = gtk.TextBuffer()
        self.insert()
        return

    def clear(self):
        self.buf.set_text("")
        self.lines = 0
        return

    def insert(self):
        self.lines += 1
        self.buf.insert(self.buf.get_end_iter(),
                        "Some text in the buffer of part1 (%d)\n" % self.lines)
        return
    
    pass  # end of class
# --------------------------------------------------------------------


class Part2Model (Model):
    counter = 0
    __observables__ = ("counter",)
    
    pass  # end of class
# --------------------------------------------------------------------


class Part3Model (Model):
    running = False
    __observables__ = ("running",)
    
    pass  # end of class
# --------------------------------------------------------------------



