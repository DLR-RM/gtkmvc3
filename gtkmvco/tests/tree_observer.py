# Copyright (C) 2013 Tobias Weber
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

import unittest

import gtk

import _importer

import gtkmvc

class Row(gtkmvc.Model):
    value = 0
    __observables__ = ('value',)

class DefaultColumn(unittest.TestCase):
    def setUp(self):
        self.store = gtk.ListStore(object, int)
        self.store.append([Row(), 0])

    def testWatch(self):
        gtkmvc.adapters.containers.watch_items_in_tree(self.store)

class CustomColumn(unittest.TestCase):
    def setUp(self):
        self.store = gtk.ListStore(int, object)
        self.store.append([1, Row()])

    def testWatch(self):
        gtkmvc.adapters.containers.watch_items_in_tree(self.store, 1)

if __name__ == "__main__":
    unittest.main()
