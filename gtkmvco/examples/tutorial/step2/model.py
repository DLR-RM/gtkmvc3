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
from gtkmvc import Model
import random

class MyModel (Model):
    """The model contains a set of counters, and only one counter is
    accessible at a time. The counter in the set must be selected
    before being used. This example shows the usage of logical
    properties, and it is used also to show how radio items like radio
    buttons or actions can be adapted easily."""

    # names of counters
    counter_names = ("First", "Second", "Third",)

    # observable properties:
    counter_select = None

    # 'counter' is a logical observable property, 'counter_select' is
    # a concrete property
    __observables__ = ('counter_select', 'counter',)

    def __init__(self):
        Model.__init__(self)
        
        self._counters = dict((name, 0) for name in MyModel.counter_names)
        # initial selected counter is choosen randomly
        self.counter_select = random.choice(MyModel.counter_names)
        return

    # ----------------------------------------------------------------------
    # The logical property depends on property 'counter_select'
    @Model.getter(deps=["counter_select"])
    def counter(self):
        return self._counters[self.counter_select] \
               if self.counter_select in self._counters else 0

    @Model.setter
    def counter(self, val):
        self._counters[self.counter_select] = val
        return
    # ----------------------------------------------------------------------


    def get_max_value(self):
        """returns the maximum value reachable by the currently
        selected counter"""
        return 5 # hard coded for simplicity


    def increment(self):
        """Increments the currently selected counter by 1. If the
        maximum value is reached, the value is not incremented."""
        if self.counter < self.get_max_value(): self.counter += 1
        return


    def reset(self):
        """Resets the currently selected counter to 0"""
        self.counter = 0
        return
        
    pass # end of class
# ----------------------------------------------------------------------
