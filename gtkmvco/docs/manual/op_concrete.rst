.. _OP_concrete:

==============================
Concrete Observable Properties
==============================

*Concrete* OPs have values stored inside the model. They are
different from *Logical* OP whose values are calculated, or come
from outside (e.g. from a database).

*Values* of OP are declared as class attributes in models, and OP
*names* are declared in a special class member
``__observables__``. ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto"
    secondname = 'Mario'
    surname = "Cavada"
    energy = 0.2 # needs holidays!
    status = "sleepy"

    __observables__ = "name surname energy".split()
    pass # end of class

In the example, ``name``, ``surname`` and ``energy`` are all
observable, whereas ``status`` is not observable.

.. _OP_concrete_patterns:

Special member ``__observables__`` is a tuple (or a list) of names
of class attributes that has to be observable. Names can contain
wildcards like ``*`` to match any sequence of characters, ``?`` to
match one single character, etc. See module `fnmatch
<http://docs.python.org/library/fnmatch.html>`_ in *Python* library
for other information about possible use of wildcards in
names. Important to say that if wildcards are used, attribute names
starting with a double underscore ``__`` will be not matched.

.. Note:: 
   It is also possible (*but deprecated!*) for the user to add a
   class variable called ``__properties__``. This variable must be
   a map, whose elements' keys are names of properties, and the
   associated values are the initial values. Using
   ``__properties__`` is complementary to the use of
   ``__observables__``, but it is provided for backward
   compatibility and should be not used in new code. 
   This is an example of usage of deprecated ``__properties__``,
   but you will not find another in this manual: ::

    from gtkmvc import Model
    class MyModelDeprecated (Model):
          __properties__ = { 
          'name' : 'Rob',
          }
          pass # end of class

This is another example showing the usage of wildcards in names: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto"
    secondname = 'Mario'
    surname = "Cavada"
    energy = 0.2 # needs holidays!
    entropy = 1.0
    enology = "good science"
    status = "sleepy"

    __observables__ = ("*name", "en????y")
    pass # end of class


In the example, all attributes but ``energy`` and ``status`` are
declared to be observable.


Concrete OP and inheritance
---------------------------

Things so far are easy enough, but they get a bit complicated when
you derive custom models from other custom models. For example,
what happens to *OP* if you derive a new model class from the class
``MyModel``?

In this case the behavior of the *OP* trusty follows the typical Object
Oriented rules:

* Any concrete *OP* in base class are inherited by derived classes.
* Derived class can override any concrete *OP* in base classes.
* If multiple base classes defines the same *OP*, only the
  first *OP* will be accessible from the derived class.


For example: ::

 from gtkmvc import Model

 class Base (Model):
    prop1 = 1
    __observables__ = ("prop1", )
 
    def __init__(self):
        Model.__init__(self)
        
         # this class is an observer of its own properties:
        self.register_observer(self) 
        return
    
    @Model.observe("prop1", assign=True)
    def prop1_changed(self, model, name, info):
        print model, "prop1 changed from '%s' to '%s'" % (info.old, info.new)
        return
    pass # end of class
 # --------------------------------------------------------
 
 class Der (Base):    
    prop2 = 2
    __observables__ = ("prop2",)
          
    @Model.observe("prop2", assign=True)
    def prop2_changed(self, model, name, info):
        print self, "prop2 changed from '%s' to '%s'" % (info.old, info.new)
        return
    pass # end of class
 # --------------------------------------------------------
 
 # test code:
 b = Base()
 d = Der() 

 d.prop2 *= 10
 d.prop1 *= 10
 b.prop1 *= 10

When executed, this script generates this output: ::

 <__main__.Der object  ...> prop2 changed from '2' to '20'
 <__main__.Der object  ...> prop1 changed from '1' to '10'
 <__main__.Base object ...> prop1 changed from '1' to '10'

Let's analyse the example. 

First, in the ``Base.__init__`` constructor you can see that the
instance registers itself as an observer... of itself! As we will see
in section :ref:`Observers`, class `Model` derives from `Observer`, so
all models are also observer. 

In the example this is exploited only to write a compact example (it
is not needed to define an additional class for the
observer). However, in complex designs it is quite common to see
models observing them self, or sub-models contained inside them.

Second, method ``Base.prop1_changed`` is explicitly marked to
observe property ``prop1``. 

Third, in class ``Der`` only the OP ``prop2`` is declared, as
``prop1`` is inherited from class ``Base``.
This is clearly visible in the output: ::

 <__main__.Der object  ...> prop1 changed from '1' to '10'

It is possible to change type and default values of OPs in derived
class, by re-declaring the OSs. For example: ::

 class Der (Base):    
    prop1 = 3
    prop2 = 2
    __observables__ = ("prop?",)

    @Observer.observe("prop2", assign=True)
    def prop2_changed(self, model, name, info):
        print self, "prop2 changed from '%s' to '%s'" % (info.old, info.new)
        return
    pass # end of class
 # --------------------------------------------------------

This would produce the output: ::

 <__main__.Der object  ...> prop2 changed from '2' to '20'
 <__main__.Der object  ...> prop1 changed from '3' to '30'
 <__main__.Base object ...> prop1 changed from '1' to '10'

As you can see, ``d.prop1`` overrides the *OP* ``prop1`` defined
in ``Base`` (they have different initial values now). 


