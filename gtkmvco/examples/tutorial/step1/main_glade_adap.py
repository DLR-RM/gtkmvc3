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

import gtk
from model import MyModel
from ctrl_glade_adap import MyControllerAdap
from view_glade import MyView

m = MyModel()
v = MyView()
c = MyControllerAdap(m, v)

gtk.main()
