#  Author: Roberto Cavada <cavada@fbk.eu>
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
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.


# ----------------------------------------------------------------------
# In this example the use of observable properties is shown.
# Somethimes the models are interested in thriggering actions into
# observers when a certain event occurs, e.g. when the model changes
# status, but it is not important to hold the new status.  In these
# situations, classical observable properties are not useful, and
# version 1.0.0 adds "signals" as special kind of observable
# properties. The example shows how signals can be used. 
# ----------------------------------------------------------------------


import _importer

from gtkmvc import ModelMT as Model
from gtkmvc.observer import Observer
import gtkmvc.observable as observable

# ----------------------------------------------------------------------
class MyModel (Model):

    __properties__ = {
        'sgn'  : observable.Signal(),
        }

    def __init__(self):
        Model.__init__(self)
        return    

    pass


# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model):
        Observer.__init__(self, model)
        return

    # notification
    def property_sgn_signal_emit(self, model, args, kwargs):
        print "Signal!", model, args, kwargs
        return

    pass # end of class

# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.sgn.emit() # we emit a signal
    m.sgn.emit("hello!") # with arguments
    pass

# ----------------------------------------------------------------------

