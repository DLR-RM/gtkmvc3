import unittest

import _importer

import gtkmvc

class Model(gtkmvc.Model):
    __observables__ = ['old', 'new', 'generic']

    def __init__(self, pre=None, post=None):
        self.calls1 = []
        gtkmvc.Model.__init__(self)
        self.calls2 = []

        self.calls1.append('init')
        self.calls2.append('init')

    def get_old_value(self):
        self.calls1.append('old')
        self.calls2.append('old')
        return 1

    @gtkmvc.Model.getter
    def new(self):
        self.calls1.append('new')
        self.calls2.append('new')
        return 2

    def get__value(self, key):
        self.calls1.append(key)
        self.calls2.append(key)
        return 3
    
class Initialization(unittest.TestCase):
    def testOrderBefore(self):
        m = Model()
        # 1.99.1
        self.assertEqual(['init'], m.calls1)

    def testOrderAfter(self):
        m = Model()
        # 1.99.1
        self.assertEqual(['init'], m.calls2)

if __name__ == "__main__":
    unittest.main()
