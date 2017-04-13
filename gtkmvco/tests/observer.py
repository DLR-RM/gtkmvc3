import unittest

import _importer
import gtkmvc

class Model(gtkmvc.Model):
    signal = gtkmvc.observable.Signal()
    iduna = gtkmvc.observable.Signal()
    value = 1
    before = None
    after = None
    __observables__ = "signal iduna value before after".split()

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.before = []
        self.after = []

class Implicit(gtkmvc.Observer):
    def property_signal_signal_emit(self, model, arg):
        self.signal = arg

    def property_value_value_change(self, model, old, new):
        self.value = old, new

    def property_before_before_change(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    def property_after_after_change(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class ImplicitVar(gtkmvc.Observer):
    def property_signal_signal_emit(self, *args):
        self.signal = args[1]

    def property_value_value_change(self, *args):
        self.value = args[1:3]

    def property_before_before_change(self, *args):
        self.before = args[2:4]

    def property_after_after_change(self, *args):
        self.after = args[2], args[4]

class Explicit(gtkmvc.Observer):
    @gtkmvc.Observer.observe("signal", signal=True)
    def notify_signal(self, model, name, info):
        self.signal = info.arg

    @gtkmvc.Observer.observe("value", assign=True)
    def notify_value(self, model, name, info):
        self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    def notify_before(self, model, name, info):
        self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("after", after=True)
    def notify_after(self, model, name, info):
        self.after = info.method_name, info.args

class ImplicitExplicit(gtkmvc.Observer):
    def __init__(self, *arg, **kwargs):
        self.calls = []
        gtkmvc.Observer.__init__(self, *arg, **kwargs)

    @gtkmvc.Observer.observe("signal", signal=True)
    def property_signal_signal_emit(self, *args):
        self.calls.append(args)

class WithNameModule(gtkmvc.Observer):
    @gtkmvc.Observer.observe("signal", signal=True, old_style_call=True)
    @gtkmvc.Observer.observe("iduna", signal=True, old_style_call=True)
    def a(self, model, prop_name, arg):
        if prop_name == "signal":
            self.signal = arg

    @gtkmvc.Observer.observe("value", assign=True)
    @gtkmvc.Observer.observe("before", assign=True)
    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

class WithName(gtkmvc.Observer):
    @gtkmvc.Observer.observe("signal", signal=True)
    @gtkmvc.Observer.observe("iduna", signal=True)
    def a(self, model, prop_name, info):
        if prop_name == "signal":
            self.signal = info.arg

    @gtkmvc.Observer.observe("value", assign=True)
    @gtkmvc.Observer.observe("before", assign=True)
    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

class DynamicWithName(gtkmvc.Observer):
    def __init__(self, model):
        gtkmvc.Observer.__init__(self)

        for name in ("signal", "iduna"): 
            self.observe(self.a, name, signal=True)
            pass
        for name in ("value", "before"):
            self.observe(self.b, name, assign=True)
            pass
        for name in ("before", "after"):            
            self.observe(self.c, name, before=True)
            pass
        for name in ("before", "after"):            
            self.observe(self.d, name, after=True)
            pass

        self.observe_model(model)

    def a(self, model, prop_name, info):
        if prop_name == "signal":
            self.signal = info.arg

    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

class Trigger(gtkmvc.Observer):
    def __init__(self, model):
        self.changes = {}
        gtkmvc.Observer.__init__(self)

        for name in ("signal", "iduna"):
            self.observe(self.a, name, signal=True)
        for name in ("value"):
            self.observe(self.a, name, assign=True)
        for name in ("before", "after"):
            self.observe(self.a, name, before=True, after=True)

        self.observe_model(model)

    def a(self, model, prop_name, info):
        try:
            self.changes[id(info)] += 1
        except KeyError:
            self.changes[id(info)] = 1

    def unique(self):
        for key in self.changes:
            if self.changes[key] > 1:
                return False
        return True

class DictionaryTest(unittest.TestCase):
    def testSafety(self):
        m = Model()
        c = Trigger(m)
        m.signal.emit(4)
        m.value = 2
        m.before.append(5)
        m.after.append(5)
        self.assertTrue(c.unique)

class SingleTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()

    def notifications(self, c):
        # TODO use getattr with default value for FAIL instead of ERROR.
        self.m.signal.emit(4)
        self.assertEqual(4, c.signal)

        self.m.value = 2
        self.assertEqual((1, 2), c.value)

        self.m.before.append(5)
        self.assertEqual(("append", (5,)), c.before)

        self.m.after.append(5)
        self.assertEqual(("append", (5,)), c.after)

    def testImplicit(self):
        self.notifications(Implicit(self.m))

    def testImplicitVar(self):
        self.notifications(ImplicitVar(self.m))

    def testExplicit(self):
        self.notifications(Explicit(self.m))

    def testWithName(self):
        self.notifications(WithName(self.m))

    def testDynamicWithName(self):
        self.notifications(DynamicWithName(self.m))

    def testWithNameModule(self):
        self.notifications(WithNameModule(self.m))

class DoubleTest(unittest.TestCase):
    def testImplicitExplicit(self):
        m = Model()
        c = ImplicitExplicit(m)
        self.assertEqual(0, len(c.calls))
        m.signal.emit("Hello")
        # Should this be 1?
        self.assertEqual(2, len(c.calls))

class Dynamic(gtkmvc.Observer):
    def a(self, model, prop_name, info):
        self.signal = info.arg

class DynamicTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.c = Dynamic()
        self.c.observe(self.c.a, "signal", signal=True)

    def testArgs(self):
        self.assertEqual(dict(signal=True),
            self.c.get_observing_method_kwargs("signal", self.c.a))

    def testGet(self):
        self.assertEqual(self.c.a,
            self.c.get_observing_methods("signal").pop())

    def testIs(self):
        self.assertTrue(self.c.is_observing_method("signal", self.c.a))
        self.assertFalse(self.c.is_observing_method("signal",
            self.c.observe_model))

    def testAdd(self):
        self.c.observe_model(self.m)
        self.m.signal.emit(4)
        self.assertEqual(4, self.c.signal)

    def testRemove(self):
        self.c.remove_observing_method(["signal"], self.c.a, )
        self.c.observe_model(self.m)
        self.m.signal.emit(4)
        self.assertFalse(hasattr(self.c, "signal"))

class DynamicMultiple(gtkmvc.Observer):
    def __init__(self, model):
        gtkmvc.Observer.__init__(self)
        self.changes = []
        for name in model.get_properties():
            self.observe(self.change, name,
                signal=True, assign=True, before=True, after=True)
        self.observe_model(model)

    def change(self, *args):
        self.changes.append(args)

class MultipleTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.c = DynamicMultiple(self.m)

    def testConstraint(self):
        # TODO also the decorator.
        self.assertRaises(ValueError,
            lambda: self.c.observe(self.c.change, "signal", signal=True))

    def testDictionary(self):
        # TODO not just for signals.
        self.m.signal.emit(4)

        model, name, info = self.c.changes.pop()

        self.assertEqual(self.m, model)
        self.assertEqual(self.m, info["model"])
        self.assertEqual("signal", name)
        self.assertEqual("signal", info["prop_name"])
        self.assertEqual(True, info["signal"])
        self.assertEqual(4, info["arg"])

        for k in info:
            self.assertEqual(info[k], getattr(info, k))

        self.assertRaises(KeyError, lambda: info["llanfairpwllgwyngyll"])
        self.assertRaises(AttributeError, lambda: info.llanfairpwllgwyngyll)

    def testNotifications(self):
        """
        Avoid regression to before r245.
        """
        self.m.signal.emit(4)
        self.assertEqual(4, self.c.changes[-1][2]["arg"])

        self.m.iduna.emit(5)
        self.assertEqual(5, self.c.changes[-1][2]["arg"])

        self.m.value = 2
        self.assertEqual(True, self.c.changes[-1][2]["assign"])

if __name__ == "__main__":
    unittest.main()
