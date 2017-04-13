# PYGTKMVC Predicate contribution
# Copyright (C) 2011  Tobias Weber
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.

import datetime

def lt(y):
    """
    For str this is equivalent to y.__gt__, but int doesn't have those slots.
    """
    return lambda x: x < y

def gt(y):
    return lambda x: x > y

def ne(y):
    return lambda x: x != y

def gtif(y):
    """
    Like gt but True if operand is None.
    """
    return lambda x: not x or x > y

def contains(y):
    """
    Case-insensitive substring search.
    """
    y = y.lower()
    return lambda x: y in x.lower()

def eqdate(y):
    """
    Like eq but compares datetime with y,m,d tuple.
    Also accepts magic string 'TODAY'.
    """
    y = datetime.date.today() if y == 'TODAY' else datetime.date(*y)
    return lambda x: x == y
