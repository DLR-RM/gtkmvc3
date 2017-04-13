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

import _importer
from gtkmvc import Model


# ----------------------------------------------------------------------
class MyModel (Model):
    """The model contains simply a counter as an observable property.
    Notice that the model is not dependant on a particular toolkit,
    and does not know it lives in a MVC chain."""

    # observable properties:
    counter = 0
    __observables__ = ('counter',)

    pass # end of class
# ----------------------------------------------------------------------
