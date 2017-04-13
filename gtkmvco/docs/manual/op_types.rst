==============================
Types of Observable Properties
==============================

In section :ref:`KOBS` we anticipated that there exist several types
of *OP*s. In the examples so far we have seen only *value* *OPs*,
meaning that observers will be notified of any change of *value*,
i.e. when the OPs are assigned to different values [#f_spurious]_.

What would happen if the value of
the property would be a complex object like a list, or a user-defined
class, and the object would change internally?

For example: ::

 from gtkmvc import Model

 class MyModel (Model):
     prop1 = [1,2,3]
     __observables__ = ("prop1",)
 
     def __init__(self):
         Model.__init__(self)
         ...
         return
     pass # end of class
 
 m = MyModel()
 m.prop1.append(4)
 m.prop1[1] = 5

Last two lines of the previous example actually change the *OP*
internally, that is different from *assigning* a new value to the
property like in ``m.prop1 = [5,4,3,2]`` that would trigger an
*assign* notifications like those seen in previous examples. Similar
problem is found when the property is assigned to a class instance,
and then a method that change the instance is called.


Supported objects
-----------------

In this section only the model-side will be presented. In the section
dedicated to observers, we will see how changes occurring to this
objects are notified.


Mutable containers
^^^^^^^^^^^^^^^^^^

The framework *MVC-O* provides a full support for python mutable
containers like *lists*, *sets*, and *maps*. For example: ::

 from gtkmvc import Model, Observer
 
 # ----------------------------------------------------------------------
 class MyModel (Model): 
     myint = 0
     mylist = []
     myset = set()
     mymap = {}
     __observables__ = ("my*", )
 
     pass # end of class
 
This covers those cases where you have your *OPs* holding mutable
sequence values. 


Class Instances
^^^^^^^^^^^^^^^

What if the value is a user-defined class instance?  Suppose a class
has a method changing the content instance. The idea is that observers
are notified when the *method* is called, with the possibility to
choose if being notified *before* or *after* the call.

However, how can the user declare that method ``M`` *does changes* the
instance? Two mechanism are provided by the framework:

* For already existing classes. In this cases the declaration occurs
  when the instance is assigned to the *OP* in the model.

* For ad-hoc and new classes. In this case the method will be
  *declared* as *Observable* at the class level, through a
  special *decorator* provided by the framework. This is the
  preferable manner. 

Examples for new classes: ::

 from gtkmvc import Model, Observable

 # ----------------------------------------------------------------------
 class AdHocClass (Observable):
     def __init__(self): 
         Observable.__init__(self)
         self.val = 0
         return
 
     # this way the method is declared as 'observed':
     @Observable.observed 
     def change(self): self.val += 1
 
     # this is NOT observed (and it does not change the instance):
     def is_val(self, val): return self.val == val
     pass #end of class
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     obj = AdHocClass()
     __observables__ = ("obj",)
 
     pass # end of class
 
As you can see, declaring a class as *observable* is as simple as
deriving from ``gtkmvc.Observable`` and decorating
those class methods that must be observed with the decorator 
``gtkmvc.Observable.observed`` (decorators are supported by
Python version 2.4 and later only). 

However, sometimes we want to reuse existing classes and it is not
possible to derive them from ``gtkmvc.Observable``. In this case
declaration of the methods to be observed can be done at time of
declaration of the corresponding *OP*. In this case the *value* to be
assigned to the *OP* must be a triple ``(class, instance,
method_names>``, where:

class
   Is the ``class`` of the object to be observed.

instance
   Is the object to be observed.

method_names
   Is a tuple of strings, representing the method
   names of the instance to be observed.

For example: ::

 from gtkmvc import Model
 #----------------------------------------------------------------------
 # This is a class the used cannot/don't want to change
 class HolyClass (object):    
     def __init__(self): self.val = 0 
     def change(self): self.val += 1
     pass #end of class
 
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     obj = (HolyClass, HolyClass(), ('change',))
     __observables__ = ("obj",)
 
     pass # end of class


Signals
^^^^^^^

Finally, *OP* can hold special values that are *signals* that can be
used to notify observers that certain *events* occurred. 

To declare an *OP* as a signal, the value of the *OP* must be an
instance of class ``gtkmvc.Signal``. To notify an event,
the model can then invoke method ``emit`` of the *OP*. Emitting a
signal can carry an optional argument.

For example: ::

 from gtkmvc import Model, Signal
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     sgn = Signal()
     __observables__ = ("sgn",)
 
     pass
  
 if __name__ == "__main__":
     m = MyModel()
     m.sgn.emit() # we emit a signal
     m.sgn.emit("hello!") # with argument
     pass
 
In the ``examples``, there are several examples that show how
different types of *OPs* can be used. Of course all available types
can be used in all available kind of model classes, with or without
multi-threading support.



Class vs Instance members as OPs
--------------------------------

So far in our examples, all OPs were class members: ::

 from gtkmvc import Model

 class MyModel (Model):
     prop1 = 10
     prop2 = []
     __observables__ = ("prop?",)
     pass # end of class

Using class vs instance attributes is not an issue when they are
assigned: ::

 m1 = MyModel()
 m2 = MyModel()
 m1.prop1 = 5
 m2.prop1 = 15

In this case after the assignment `m1` and `m2` will have their own
value for attribute `prop1`.

However, when dealing with attributes whose type is a class instances,
like for example a list, you must keep in mind the attribute sharing. ::

 m1.prop2.append(1)
 print m2.prop2 # prints [1] !

If attribute sharing is not what you want, simply assign OPs in the
model's constructor: ::

 class MyModel (Model):
     prop1 = 10
     prop2 = [] # may be any value actually
     __observables__ = ("prop?",)

     def __init__(self):
       MyModel.__init__(self)
       self.prop2 = []
       return
     pass # end of class

Now `m1.prop2` and `m2.prop2` are different objects, and sharing no
longer occurs.

.. rubric:: Section Notes
.. [#f_spurious] Actually there exist *spurious* assign notifications,
                 which are issued also when there is no change in the
                 value of an OP, e.g. when an OP is assigned to
                 itself.
