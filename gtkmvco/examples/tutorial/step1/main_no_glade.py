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

import gtk
from model import MyModel
from ctrl_no_glade import MyControllerNoGlade
from view_no_glade import MyViewNoGlade

m = MyModel()
v = MyViewNoGlade()
c = MyControllerNoGlade(m, v)

gtk.main()
