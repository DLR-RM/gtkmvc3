"""
Test for Observer.observe() with patterns in property name
(see ticket:31)
"""

import _importer
from gtkmvc import Model, Observer

import operator
import unittest


class MyModel (Model):
    conc1 = 0
    conc2 = 0
    conc3 = 0
    __observables__ = ("conc?",)    
# ----------------------------------------------------------------------

# internal service for notifications

# decorator for tracked notification methods

class MyObserverAbstract (Observer):
    @classmethod
    def _tracked(cls, meth):
        def _notify(self, model, name, info):
            self.notif.append(info)
            meth(self, model, name, info)
            return
        return _notify    

    def __init__(self, model=None):
        Observer.__init__(self, model)
        self.notif = []
        return

    def count(self, prop_name):
        # returns the number of times prop_name has been notified
        return map(operator.attrgetter("prop_name"), self.notif).count(prop_name)
    
    pass # end of class
# ----------------------------------------------------------------------


class MyObserverBase (MyObserverAbstract):

    @Observer.observe("conc[13]", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc1(self, model, name, info): return
        
    @Observer.observe("conc[23]", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc2(self, model, name, info): return
    pass # end of class
# ----------------------------------------------------------------------

class MyObserverDer (MyObserverBase):
    @Observer.observe("conc*", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc12(self, model, name, info): return
    pass # end of class
# ----------------------------------------------------------------------

class MyObserverBaseDyn (MyObserverAbstract):
    @MyObserverAbstract._tracked
    def notify_dyn(self, model, name, info): return
    pass # end of class

class MyObserverDerDyn (MyObserverDer):
    @MyObserverAbstract._tracked
    def notify_dyn(self, model, name, info): return
    pass # end of class
# ----------------------------------------------------------------------


class MyObserverErr1 (MyObserverDer):
    @Observer.observe("conc1", assign=True)
    @Observer.observe("conc[23]", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc_err(self, model, name, info): return
    pass # end of class

class MyObserverErr2 (MyObserverDer):
    @Observer.observe("conc[23]", assign=True)
    @Observer.observe("conc1", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc1_err(self, model, name, info): return
    pass # end of class

class MyObserverErr3 (MyObserverDer):
    @Observer.observe("conc[23]", assign=True)
    @Observer.observe("conc*", assign=True)
    @MyObserverAbstract._tracked
    def notify_conc1_err(self, model, name, info): return
    pass # end of class
# ----------------------------------------------------------------------

class ObserveWithPatterns (unittest.TestCase):
    
    def setUp(self):
        self.m = MyModel()
        return

    def test_base_conc3_static(self):
        o = MyObserverBase(self.m)
        self.m.conc3 += 1
        for n,c in { "conc1" : 0,
                     "conc2" : 0,
                     "conc3" : 2 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_base_conc123_static(self):
        o = MyObserverBase(self.m)
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 1,
                     "conc2" : 1,
                     "conc3" : 2 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_conc3_static(self):
        o = MyObserverDer(self.m)
        self.m.conc3 += 1
        for n,c in { "conc1" : 0,
                     "conc2" : 0,
                     "conc3" : 3 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_conc123_static(self):
        o = MyObserverDer(self.m)
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 2,
                     "conc2" : 2,
                     "conc3" : 3 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_dyn_no_pat_check(self):
        for klass in (MyObserverBaseDyn, MyObserverDerDyn):
            o = klass()
            o.observe(o.notify_dyn, "conc3", assign=True)
            o.observe_model(self.m)
            self.assert_(o.is_observing_method("conc3", o.notify_dyn))
            pass
        return

    def test_der_dyn_pat_check(self):
        for klass in (MyObserverBaseDyn, MyObserverDerDyn):
            o = klass()
            o.observe(o.notify_dyn, "conc[234]", assign=True)
            o.observe_model(self.m)
            for prop in "conc2 conc3 conc4".split():
                self.assert_(o.is_observing_method(prop, o.notify_dyn))
                pass
            pass
        return

    def test_der_conc123_dyn_no_pat(self):
        o = MyObserverDerDyn()
        o.observe(o.notify_dyn, "conc3", assign=True)
        o.observe_model(self.m)
        
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 2,
                     "conc2" : 2,
                     "conc3" : 4 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_conc123_dyn_pat_check(self):
        o = MyObserverDerDyn()
        o.observe(o.notify_dyn, "conc[2345]", assign=True)
        o.observe_model(self.m)
        
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 2,
                     "conc2" : 3,
                     "conc3" : 4 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_conc123_base_dyn_pat_remove(self):
        o = MyObserverBaseDyn()
        o.observe(o.notify_dyn, "conc[12345]", assign=True)
        o.remove_observing_method(("conc2", "conc3"), o.notify_dyn)
        o.observe_model(self.m)
        
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 1,
                     "conc2" : 0,
                     "conc3" : 0 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return

    def test_der_conc123_base_dyn_pat_remove(self):
        o = MyObserverDerDyn()
        o.observe(o.notify_dyn, "conc[12345]", assign=True)
        o.remove_observing_method(("conc2", "conc3"), o.notify_dyn)
        o.observe_model(self.m)
        
        self.m.conc1 += 1
        self.m.conc2 += 1
        self.m.conc3 += 1
        for n,c in { "conc1" : 2,
                     "conc2" : 2,
                     "conc3" : 3 }.iteritems():
            self.assertEqual(o.count(n), c)
            pass
        return
    
    def test_errors(self):
        # syntax errors about patterns are found
        for klass in (MyObserverErr1, MyObserverErr2, MyObserverErr3):
            self.assertRaises(ValueError, klass)
        return
    pass # end of class
# ----------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

