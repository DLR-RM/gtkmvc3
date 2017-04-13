# PYGTKMVC SQLObject sample
# Copyright (C) 2010  Tobias Weber
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

"""
Like sql.py but passing connection instances explicitly so we can have more
than one. Useful to implement "Save As". Test should print:
<Person 2 fname='John' mi=None lname='Doe'>
<Person 2 fname='Kyle' mi=None lname='Elo'>
"""
import _importer

from sqlobject import *

from gtkmvc.model import SQLObjectModel
from gtkmvc import Observer

# WARNING we overwrite existing files and don't clean up afterwards.
c1 = connectionForURI('sqlite:///tmp/doc1')
c2 = connectionForURI('sqlite:///tmp/doc2')

class Person (SQLObjectModel):
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observables__ = ['?name']
  pass

#http://www.sqlobject.org/SQLObject.html#transactions
SQLObjectModel.createTables(ifNotExists=True, connection=c1)
SQLObjectModel.createTables(ifNotExists=True, connection=c2)

p = Person(fname="John", lname="Doe", connection=c1)
q = Person(fname="Kyle", lname="Elo", connection=c2)
print p
print q
