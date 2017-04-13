"""
Test for checking spuriousness of observers works
"""

import _importer
from gtkmvc import Model, Observer
import unittest

# ----------------------------------------------------------------------
class MyModel (Model):
    prop1 = 0
    prop2 = 0
    __observables__ = ("prop[12]", )
    pass # end of class

# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model=None, spurious=False):
        Observer.__init__(self, model, spurious=spurious)
        self.notif = []
        return

    def count(self, name): return self.notif.count(name)

    @Observer.observe("prop?", assign=True)
    def static_notify(self, model, name, info):
        self.notif.append(name)
        return

    # for dynamic notifications
    def dynamic_notify(self, model, name, info):
        self.notif.append(name)
        return

    pass # end of class
    
# ----------------------------------------------------------------------

class MyObserverForced (MyObserver):
    @Observer.observe("prop1", assign=True, spurious=False)
    @Observer.observe("prop2", assign=True)
    def static_notify_prop1_forced_no(self, model, name, info):
        self.notif.append(name)
        return

    @Observer.observe("prop1", assign=True, spurious=True)
    @Observer.observe("prop2", assign=True)
    def static_notify_prop1_forced_yes(self, model, name, info):
        self.notif.append(name)
        return
    pass # end of class
    
# ----------------------------------------------------------------------
    

class SpuriousnessTest(unittest.TestCase):
    def setUp(self):
        self.m = MyModel()
        return

    # static:
    def test_static_default_no(self):
        o = MyObserver(self.m, False)
        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 0,
                     "prop2" : 0
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    def test_static_default_yes(self):
        o = MyObserver(self.m, True)
        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 1,
                     "prop2" : 1
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    def test_static_forced_no(self):
        o = MyObserverForced(self.m, False)
        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 1,
                     "prop2" : 0
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    def test_static_forced_yes(self):
        o = MyObserverForced(self.m, True)
        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 2,
                     "prop2" : 3
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    # dynamic:
    def test_dynamic_default_no(self):
        o = MyObserver(spurious=False)
        o.observe(o.dynamic_notify, "prop?", assign=True)
        o.observe_model(self.m)
        
        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 0,
                     "prop2" : 0
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    def test_dynamic_default_yes(self):
        o = MyObserver(spurious=True)
        o.observe(o.dynamic_notify, "prop?", assign=True)
        o.observe_model(self.m)

        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 2,
                     "prop2" : 2
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    def test_dynamic_forced_no(self):
        o = MyObserverForced(spurious=False)
        o.observe(o.dynamic_notify, "prop1", assign=True, spurious=True)
        o.observe(o.dynamic_notify, "prop2", assign=True)
        o.observe_model(self.m)

        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 2,
                     "prop2" : 0
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    # must be identical to the previous
    def test_dynamic_forced_no_explicit(self):
        o = MyObserverForced(spurious=False)
        o.observe(o.dynamic_notify, "prop1", assign=True, spurious=True)
        o.observe(o.dynamic_notify, "prop2", assign=True, spurious=False)
        o.observe_model(self.m)

        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 2,
                     "prop2" : 0
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return


    def test_dynamic_forced_yes(self):
        o = MyObserverForced(spurious=True)
        o.observe(o.dynamic_notify, "prop1", assign=True)
        o.observe(o.dynamic_notify, "prop2", assign=True, spurious=False)
        o.observe_model(self.m)

        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 3,
                     "prop2" : 3
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    # must be identical to the previous
    def test_dynamic_forced_yes_explicit(self):
        o = MyObserverForced(spurious=True)
        o.observe(o.dynamic_notify, "prop1", assign=True, spurious=True)
        o.observe(o.dynamic_notify, "prop2", assign=True, spurious=False)
        o.observe_model(self.m)

        self.m.prop1 += 0
        self.m.prop2 += 0

        for n,v in { "prop1" : 3,
                     "prop2" : 3
                     }.iteritems():
            self.assertEqual(o.count(n), v)
            pass
        return

    pass # end of class

if __name__ == "__main__":
    unittest.main()
