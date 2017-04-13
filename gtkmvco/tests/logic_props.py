"""
Test for getter and setter decorators, used in models to define 
logical properties
"""

# THIS IS ON_GOING WORK

import _importer
from gtkmvc import Model

import unittest

class MyModel (Model):

    prop1 = 1 # concrete
    __observables__ = "prop1 prop2 prop3 prop4 prop5 prop6 "\
        "prop7 prop8 prop9 prop10 prop11".split()    
        
    _prop2 = 2
    # pure old style
    def get_prop2_value(self): return self._prop2
    def set_prop2_value(self, val): self._prop2 = val
    
    # old-style read only
    def get_prop3_value(self): return 3
    
    _prop4 = 4
    # mixed old-style and new style
    def get_prop4_value(self): return self._prop4
    @Model.setter
    def prop4(self, val): self._prop4 = val

    _prop5 = 5
    # like before, but inverted
    def set_prop5_value(self, val): self._prop5 = val
    @Model.getter
    def prop5(self): return self._prop5

    # pure new style (explicit)
    _prop6 = 6
    @Model.getter
    def prop6(self): return self._prop6
    @Model.setter
    def prop6(self, val): self._prop6 = val

    _prop7 = 7
    # mixed old/new style with names
    def set_prop7_value(self, val): self._prop7 = val
    @Model.getter("prop7")
    def prop7_named(self, name): 
        assert "prop7" == name
        return self._prop7

    _prop8 = 8
    # like before, but inverted
    def get_prop8_value(self): return self._prop8
    @Model.setter("prop8")
    def prop8_named(self, name, val): 
        assert "prop8" == name
        self._prop8 = val
        return
    
    _prop9 = 9
    _prop10 = 10
    # pure, named
    @Model.getter("prop9", "prop10")
    def get_prop9_10_named(self, name): 
        return {"prop9" : self._prop9, "prop10" : self._prop10}[name]

    @Model.setter("prop9", "prop10")
    def set_prop9_10_named(self, name, val): 
        if "prop9" == name: self._prop9 = val
        elif "prop10" == name: self._prop10 = val
        else: assert False, name
        return
    
    _prop11 = 11
    # generic old style
    def get__value(self, name):
        return {"prop11" : self._prop11}[name]
    def set_prop11_value(self, val):
        self._prop11 = val
        return
        

    pass # end of class
# ----------------------------------------------------------------------


class MyModelDerEmpty (MyModel): pass

class MyModelDerOverload (MyModelDerEmpty):
    def get_prop2_value(self): 
        return MyModelDerEmpty.get_prop2_value(self) * 4

    def set_prop2_value(self, val): 
        MyModelDerEmpty.set_prop2_value(self, val/2)
        return

    def get__value(self, name):
        return {"prop11" : self._prop11}[name] * 2
    pass # end of class


class MyModelDerOverwrite(MyModelDerOverload):
    __observables__ = ("prop1", "prop3", "prop11")

    @Model.getter
    def prop1(self): return 100
    @Model.setter
    def prop1(self, val): return

    _prop3 = 200
    @Model.getter
    def prop3(self): return self._prop3
    @Model.setter
    def prop3(self, val): self._prop3 = val
        
    @Model.getter
    def prop11(self): return 300
    @Model.setter("prop11")
    def prop11(self, name, val): 
        assert "prop11" == name
        pass
    pass # end of class

    

class LogicalProps(unittest.TestCase):
    def setUp(self): 
        return
        
    # checks that metaclass creates all properties
    def test_base_class_properties_have_been_created(self):
        for name in MyModel.__observables__:
            self.assert_(hasattr(MyModel, name))
            if name != "prop1":
                self.assert_(isinstance(getattr(MyModel, name), property))
                pass
            pass
        return

    # checks that all properties can be read
    def test_base_instance_properties_can_be_read(self):
        m = MyModel()
        for idx, name in enumerate(m.__observables__):
            self.assertEqual(getattr(m, name), idx+1)
            pass
        return

    # checks that all properties (but readonly) can be written
    def test_base_instance_properties_can_be_written(self):
        m = MyModel()
        for idx, name in enumerate(m.__observables__):
            if name != "prop3": setattr(m, name, idx+10)
            pass

        for idx, name in enumerate(m.__observables__):
            if name != "prop3": self.assertEqual(getattr(m, name), idx+10)
            else: self.assertEqual(getattr(m, name), idx+1)
            pass
        return

    # check readonly
    def test_base_instance_prop3_is_readonly(self):
        m = MyModel()
        val = m.prop3
        def foo(m, val): m.prop3 = val
        self.assertRaises(AttributeError, foo, m, val)
        self.assertEqual(m.prop3, val)
        return

    # all properties are accessible from epty derived classes
    def test_der_empty(self):
        m = MyModelDerEmpty()
        for idx, name in enumerate(m.__observables__):
            self.assertEqual(getattr(m, name), idx+1)
            pass
        return

    # checks that overloading of getter/setter works
    def test_der_overload(self):
        m = MyModelDerOverload()
        self.assertEqual(m.prop2, 8)
        m.prop2 = 10
        self.assertEqual(m.prop2, 20)

        m.prop11 = 20
        self.assertEqual(m.prop11, 40)
        return

    # properties can be overwritten in derived classes
    def test_der_overwrite(self):
        m = MyModelDerOverwrite()
        self.assertEqual(m.prop1, 100)
        self.assertEqual(m.prop3, 200)
        self.assertEqual(m.prop11, 300)

        m.prop1 = 200
        self.assertEqual(m.prop1, 100)

        m.prop3 = 300
        self.assertEqual(m.prop3, 300)

        m.prop11 = 400
        self.assertEqual(m.prop11, 300)
        return

    pass


if __name__ == "__main__":
    unittest.main()
