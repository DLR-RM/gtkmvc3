"""
Ticket #49

Allow inconsistent internal state as long as there are no observers yet.
"""

import unittest

import _importer

from gtkmvc import Model

class M(Model):
    concrete = None

    __observables__ = ('concrete', 'logical')

    @Model.getter(deps=['concrete'])
    def logical(self):
        raise RuntimeError

    def __init__(self):
        Model.__init__(self)
        self.concrete = 1

class Test(unittest.TestCase):
    def test(self):
        M()

if __name__ == "__main__":
    unittest.main()
