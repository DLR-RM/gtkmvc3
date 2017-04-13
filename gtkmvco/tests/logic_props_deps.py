"""
Test for dependencies of logical properties
"""

import _importer
from gtkmvc import Model, Observer

import unittest

class LinearSingleLevel (Model):
    # basic, single level linear dependency
    conc = 0

    __observables__ = "conc log1 log2".split()

    @Model.getter(deps=["conc"])
    def log1(self): return self.conc+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.log1+1
    pass

class DerivedModel (LinearSingleLevel):
    # to check that derivation works
    __observables__ = ("log3",)
    
    @Model.getter(deps=["log2"])
    def log3(self): return self.log2+1
    pass

class DerivedModelWithOverriding (LinearSingleLevel):
    # to check that derivation works. here the dependency chain is
    # interrupted at log1
    __observables__ = ("log3", "log1")

    @Model.getter # log1 no longer depends on conc
    def log1(self): return 0

    @Model.setter
    def log1(self, val): return # dummy
    
    @Model.getter(deps=["log2"])
    def log3(self): return self.log2+1
    pass

class LinearSingleLevelPattern (Model):
    # basic, single level linear dependency, use of patterns in
    # decorators
    conc = 0

    __observables__ = "conc log1 log2".split()

    @Model.getter("log?", deps=["conc"])
    def log12_get(self, name): return self.conc+1

class LinearMultiLevel (Model):
    # more complex linear dependency    
    conc = 0

    __observables__ = "conc log1 log2 log3".split()

    @Model.getter(deps=["conc"])
    def log1(self): return self.conc+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.log1+1

    @Model.getter(deps=["log2"])
    def log3(self): return self.log2+1

    @Model.setter("log2", "log1")
    def _setter(self, name, val):
        return # dummy
    
    pass

class LinearMultiLevelWithSetter (Model):
    # Like LinearMultiLevel, but this is used to check that multiple
    # spurious notifications are handled correctly. Here we set log2
    # so log2 (and log3 if spurious notifications are enabled) should
    # be notified. However, setter for log2 sets conc, so another
    # chain of notifications is added (conc, log1, and again log2 and
    # log3). The second notifications for log2 and log3 are not sent
    # as they were sent already.
    
    conc = 0

    __observables__ = "conc log1 log2".split()

    @Model.getter(deps=["conc"])
    def log1(self): return self.conc+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.log1+1

    @Model.getter(deps=["log2"])
    def log3(self): return self.log2+1

    @Model.setter("log1", "log2")
    def _setter(self, name, val):
        self.conc = val - {"log1" : 1,
                           "log2" : 2,}[name]
        return    
    pass


class BranchSingleLevel (Model):
    # with branch, each dependency is a tree with height 1
    conc1 = 0
    conc2 = 1

    __observables__ = "conc? log1 log2 log3".split()
    
    @Model.getter(deps=["conc1"])
    def log1(self): return self.conc1+1

    @Model.getter(deps=["conc1"])
    def log2(self): return self.conc1+1

    @Model.getter(deps=["conc1", "conc2"])
    def log3(self): return self.conc1+self.conc2
    pass

class BranchMultiLevel (Model):
    # here each dependency is a graph, and there is a diamond
    # (conc1,log1,log2) to test that multiple spurious notifications
    # are not done.
    # ======================
    #   +-> conc1   conc2
    #   |     ^       ^
    #   |     |       |
    #   |    log1     |
    #   |     ^       |
    #   |     |       |
    #   +--- log2 ----+
    #         ^
    #         |
    #        log3
    # ======================
    conc1 = 0
    conc2 = 1

    __observables__ = "conc? log1 log2 log3".split()
    
    @Model.getter(deps=["conc1"])
    def log1(self): return self.conc1+1

    # here there is a diamond
    @Model.getter(deps=["conc1", "conc2", "log1"])
    def log2(self): return self.conc1+self.conc2+self.log1

    @Model.getter(deps=["log2"])
    def log3(self): return self.log2    
    pass


class LinearSingleLevelOldStyle (Model):
    # basic, single level linear dependency
    conc = 0
    __observables__ = "conc log1 log2".split()

    # specific
    def get_log1_value(self, deps=["conc"]): return self.conc+1

    # general
    def get__value(self, name, deps=["log1"]):
        assert "log2" == name
        return self.log1+1
    pass


# must raise ValueError
class InvalidLoop (Model):
    conc = 0
    __observables__ = "conc log1 log2 log3".split()

    @Model.getter(deps=["conc1", "log3"])
    def log1(self): return self.conc1+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.conc1+1

    @Model.getter(deps=["log2"])
    def log3(self): return self.conc1+1
    pass

class NonExisting (Model):
    # should raise ValueError, as deps refers to non-existant property
    __observables__ = ("log1",)
    
    @Model.getter(deps=["non-existing"])
    def log1(self): return 0
    pass

def make_ErroneousType():
    # factory for ErroneousType. Factory is needed here as this is
    # checked at compile time otherwise
    class ErroneousType (Model):
        # should raise TypeError, as using wrong type for name of
        # property in deps.
        __observables__ = ("log1",)
        erroneous_type_value = 1
        @Model.getter(deps=erroneous_type_value)
        def log1(self): return 0
        pass
    return ErroneousType

def make_ErroneousTypeElement():
    # factory for ErroneousType. Factory is needed here as this is
    # checked at compile time otherwise
    class ErroneousTypeElement (Model):
        # should raise TypeError, as using wrong type for name of
        # property in deps.
        __observables__ = ("log1",)
        erroneous_type_value = 1
        @Model.getter(deps=(erroneous_type_value,))
        def log1(self): return 0
        pass
    return ErroneousType

def make_ErroneousTypeOldStyle():
    # factory for ErroneousTypeOldStyle. Factory is needed here as this is
    # checked at compile time otherwise
    class ErroneousTypeOldStyle (Model):
        # should raise TypeError, as using wrong type for name of
        # property in deps.
        __observables__ = ("log1",)
        erroneous_type_value = 1

        def get_log1_value(self, deps=erroneous_type_value): return 0
        pass
    return ErroneousType

def make_ErroneousTypeElementOldStyle():
    # factory for ErroneousTypeElementOldStyle. Factory is needed here
    # as this is checked at compile time otherwise
    class ErroneousTypeElementOldStyle (Model):
        # should raise TypeError, as using wrong type for name of
        # property in deps.
        __observables__ = ("log1",)
        erroneous_type_value = 1

        def get__value(self, name, deps=(erroneous_type_value,)): return 0
        pass
    return ErroneousType

# ----------------------------------------------------------------------

class MyObserver (Observer):
    # the observers simply keeps track of received notifications
    def __init__(self, spurious):
        Observer.__init__(self, spurious=spurious)
        self.rec = []
        return
    
    @Observer.observe("conc", assign=True)
    @Observer.observe("conc1", assign=True)
    @Observer.observe("conc2", assign=True)
    @Observer.observe("log1", assign=True)
    @Observer.observe("log2", assign=True)
    @Observer.observe("log3", assign=True)
    def notify(self, model, name, info):
        self.rec.append(name)
        return
    pass 
# ----------------------------------------------------------------------


class LogicalPropsDeps (unittest.TestCase):
    def setUp(self):
        # there are two observers, only one accepts spurious
        # notifications.
        self.o1 = MyObserver(spurious=False)
        self.o2 = MyObserver(spurious=True)
        return

    def __model_factory(self, model_class):
        m = model_class()
        for o in (self.o1, self.o2): o.observe_model(m)
        return m
    
    # --------------------  TESTS --------------------
    def test_single_linear(self):
        m = self.__model_factory(LinearSingleLevel)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in m.get_properties():                
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass
        return

    def test_multi_linear(self):
        m = self.__model_factory(LinearMultiLevel)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in m.get_properties():                
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass
        return

    def test_multi_linear_middle(self):
        m = self.__model_factory(LinearMultiLevel)
        m.log2 += 1

        for o in (self.o1, self.o2):            
            for p in m.get_properties():
                self.assertEqual(o.rec.count(p),
                                 {'conc' : 0,
                                  'log1' : 0,
                                  'log2' : 1,
                                  'log3' : int(o.accepts_spurious_change()),
                                  }[p])
                pass
            pass
        return

    def test_multi_linear_middle_with_setter(self):
        m = self.__model_factory(LinearMultiLevelWithSetter)
        m.log2 += 1

        for o in (self.o1, self.o2):            
            for p in m.get_properties():
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass
        return

    def test_single_branch_from_conc1(self):
        m = self.__model_factory(BranchSingleLevel)
        m.conc1 += 1

        for o in (self.o1, self.o2):
            for p, v in {"conc1" : 1,
                         "conc2" : 0,
                         "log1" : 1,
                         "log2" : 1,
                         "log3" : 1}.iteritems():
                self.assertEqual(o.rec.count(p), v)
                pass
            pass        
        return

    def test_single_branch_from_conc2(self):
        m = self.__model_factory(BranchSingleLevel)
        m.conc2 += 1

        for o in (self.o1, self.o2):
            for p, v in {"conc1" : 0,
                         "conc2" : 1,
                         "log1" : 0,
                         "log2" : 0,
                         "log3" : 1}.iteritems():
                self.assertEqual(o.rec.count(p), v)
                pass
            pass        
        return
    
    def test_multi_branch_from_conc1(self):
        m = self.__model_factory(BranchMultiLevel)
        m.conc1 += 1

        for o in (self.o1, self.o2):
            for p, v in {"conc1" : 1, # *
                         "conc2" : 0,
                         "log1" : 1, # *
                         "log2" : 1, # *
                         "log3" : 1}.iteritems():
                self.assertEqual(o.rec.count(p), v)
                pass
            pass
        # (*) diamond is handled
        return

    def test_loop_detected(self):
        self.assertRaises(ValueError, InvalidLoop)
        return

    def test_non_existing_detected(self):
        self.assertRaises(ValueError, NonExisting)
        return

    def test_erroneous_type1(self):
        self.assertRaises(TypeError, make_ErroneousType)
        return

    def test_erroneous_type2(self):
        self.assertRaises(TypeError, make_ErroneousTypeElement)
        return

    def test_derivation1(self):
        m = self.__model_factory(DerivedModel)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in "conc log1 log2 log3".split():
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass
        return

    def test_derivation2(self):
        m = self.__model_factory(DerivedModelWithOverriding)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in "conc log1 log2 log3".split():
                self.assertEqual(o.rec.count(p),
                                 {'conc' : 1,
                                  'log1' : 0,
                                  'log2' : 0,
                                  'log3' : 0
                                  }[p])
                pass
            pass        
        return

    def test_derivation3(self):
        m = self.__model_factory(DerivedModelWithOverriding)
        m.log1 += 1

        for o in (self.o1, self.o2):
            for p in "conc log1 log2 log3".split():
                self.assertEqual(o.rec.count(p),
                                 {'conc' : 0,
                                  'log1' : 1,
                                  'log2' : int(o.accepts_spurious_change()),
                                  'log3' : int(o.accepts_spurious_change()),
                                  }[p])
                pass
            pass        
        return

    def test_pattern(self):
        m = self.__model_factory(LinearSingleLevelPattern)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in "conc log1 log2".split():
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass     
        return

    def test_single_linear_old_style(self):
        m = self.__model_factory(LinearSingleLevelOldStyle)
        m.conc += 1

        for o in (self.o1, self.o2):
            for p in m.get_properties():                
                self.assertEqual(o.rec.count(p), 1)
                pass
            pass
        return

    def test_erroneous_old_style_type1(self):
        self.assertRaises(TypeError, make_ErroneousTypeOldStyle)
        return

    def test_erroneous_old_style_type2(self):
        self.assertRaises(TypeError, make_ErroneousTypeElementOldStyle)
        return
        
    
    pass # end of class


if __name__ == "__main__":
    unittest.main()


