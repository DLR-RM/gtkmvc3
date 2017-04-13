.. _Observers:

=========
Observers
=========

If OPs live into ``Models``, ``Observers`` are the objects which are
interested in being notified when an OP gets changed. An Observer
observes one or more Models.

A typical observer is an instance of class :ref:`gtkmvc.Controller<CONTROLLERS>` which
derive from :class:`gtkmvc.Observer`.

Also :ref:`gtkmvc.Model<MODELS>` derives from :class:`gtkmvc.Observer`, as
in hierarchies of models parents sometimes observe children.

.. Important::

   Since version 1.99.1, observers were deeply revised. If you have
   experience with older versions, you will find many changes,
   although all changes are backward compatible. In particular the
   usage of name-based notification methods like
   ``property_<name>_value_change`` is discouraged, but still
   supported for backward compatibility. At the end of this section
   all discouraged/deprecated features about observers are listed.



Observer registration
---------------------

Registration is the mechanism which observers make model known about
them. 

There are a few methods which can be used when registering observers into models.

.. method:: Observer.__init__(model=None, spurious=False)
 
   Class constructor

   :param model: is optional ``Model`` to observe.
   :param spurious: when ``True`` make the interested in receiving
   	  	    spurious notifications, i.e. when an obxserved OP
   	  	    is assigned with the same value it got before the
   	  	    assignment.

.. method::  Observer.observe_model(model)

   Observes the given model among the others already observed.

   :param model: the Model instance to observe.

.. method::  Observer.relieve_model(model)

   Stops observing the given model which was being previously observed.

   :param model: the Model instance to relieve.

Since it is common to observe one model, the class constructor provides
the possibility to specify it.


Change Notifications
--------------------

When an OP gets changed, notifications are sent by the framework to
observer's methods. As we see in previous chapter, changes can happen
at:

Assignment
	When the value of an OP is changed, meaning that the OP is
	assigned with a value.

Instance 
	 When an object instance is changed internally. For example an
	 element is added to a list, or a method modifying the
	 instance is called.


.. _Observer_vcn:

Change Notification Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Independently on the notification type, the prototype of notification
methods in observers is always:

.. method:: Observer.method_name(model, prop_name, info)

   :param model: is the observed Model instance containing the OP
                 which got changed

   :param prop_name: is the name of the OP which got changed.

   :param info: a dictionary whose content depends on the notification
                type (namely *assign*, *before* method call, *after* method
                call and *signal*).

How is an observer's method declared to be *notification* method for
an OP? It is possible to declare notification methods *statically* or
*dynamically*.

1. **Statically** with decorator ``@Observer.observe``. For example::

    from gtkmvc import Observer
    class MyObserver (Observer):

      @Observer.observe('prop1', assign=True)
      @Observer.observe('prop2', assign=True, signal=True)
      def notifications(self, model, prop_name, info):
          # this is called when 'prop1' or 'prop2' are assigned
          # and also when 'prop2.emit()' is called
          return

      @Observer.observe('prop1', assign=True)
      def other_notification(self, model, prop_name, info):
          # this is called when 'prop1' is assigned
          return

   Notice that an OP can be bound to multiple notifications, like
   ``prop1`` in the example. Also notice that the type of the
   notification (assign, signal, etc.) is declared by means of keyword
   arguments flags. We are discussing types and keyword arguments
   later in this section.

2. **Dynamically** with method ``Observer.observe``. For example::

    from gtkmvc import Observer
    class MyObserver (Observer):

      def __init__(self):
         Observer.__init__(self)

         self.observe(self.notification, "prop1", assign=True)
         self.observe(self.notification, "prop2", assign=True, signal=True)
         return

      def notification(self, model, prop_name, info):
          # ...
          return

   As you can see, `Observer.observe` can be used both as decorator
   and instance method to declare notifications. When used dynamically
   (as instance method), the only difference is that it takes as first
   argument the method to declare as notification.

   Class `Observer` provides some other methods wich are useful when
   dealing with dynamic definition of notifications. In particular:

   .. method:: def get_observing_methods(self, prop_name)

      Returns a set of methods which have been registered as
      notifications for a property.

      :param prop_name: the name of the property.
      :returns: a set of methods.


   .. method:: def remove_observing_method(self, prop_names, method)

      Removes a previously defined notification method for a property
      set.

      :param prop_names: sequence of names of properties.
      :param method: The method previously defined as a notification. 

   .. method:: def is_observing_method(self, prop_names, method)

      Returns True if given method is a notification for given
      property name.

      :param prop_name: name of the property.
      :param method: The method whose nature is queried. 
      :returns: a boolean value.


   .. Warning::

      Version 1.99.1 does not provide a full support for definition of
      dynamic behaviours yet. In particular it is necessary at the
      moment to declare dynamic notifications *before* registering the
      models the notifications are interested in. Next version will
      provide a better support.
   

Use of patterns with `Observer.observe`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since version 1.99.2 it is possible to use patterns instead of the
property name, like in :ref:`Concrete OP<OP_Concrete>` which
can be specified using :ref:`patterns<OP_concrete_patterns>`. 

The property name can contain wildcards like ``*`` to match any
sequence of characters, ``?`` to match one single character, etc. See
module `fnmatch <http://docs.python.org/library/fnmatch.html>`_ in
*Python* library for other information about possible use of wildcards
in names.

With patterns it is possible to declare notification methods which are
called for properties whose names match a syntactical rule. For
example::

   from gtkmvc import Observer
   class MyObserver (Observer):

      @Observer.observe('prop[1234]', assign=True, signal=True)
      def notifications(self, model, prop_name, info):
          # this is called when 'prop1', 'prop2', 'prop3' and 'prop4'
          # are assigned and also when 'prop[1234].emit()' is called
          return

      @Observer.observe('a*', assign=True)
      def other_notification(self, model, prop_name, info):
          # this is called when any observed property whose name
          # begins with 'a' is assigned
          return

      @Observer.observe('*', after=True)
      def all_notification(self, model, prop_name, info):
          # this is called after any observed property is changed by a method
          return

      # this is used to add a notification at runtime
      def a_method(self, model, prop_name, info):
          return

Patterns can be used also when `Observer.observe` is called to add
notifications at runtime::

  o = MyObserver()
  o.observe(o.a_method, "prop?", assign=True)

.. Important::

   When patterns are used with `Observer.observe`, each notification
   method can have only **one** `Observer.observe` call or decorator,
   or exception `ValueError` is raised when the class is instantiated
   (for decorators), or when `Observer.observe` is called (for dynamic
   declarations). For example this is **not** allowed::

    from gtkmvc import Observer
    class MyObserver (Observer):

      # ERROR
      @Observer.observe('a*', assign=True)
      @Observer.observe('prop[1234]', signal=True)
      def notifications(self, model, prop_name, info):
          #...
          return

      # ERROR
      @Observer.observe('prop1', assign=True)
      @Observer.observe('prop[1234]', signal=True)
      def notifications(self, model, prop_name, info):
          #...
          return

.. versionadded:: 1.99.2
     

The parameter `info:NTInfo`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We anticipated that parameter `info` of change notification is a
dictionary whose content depends on the notification type. Actually
:obj:`info` is an instance of class :class:`NTInfo` 
(**N**\ otification **T**\ ype **Info**\ rmation).

:class:`NTInfo` derives from :class:`dict` type, but offers the
possibility to access to its values by accessing keys as attributes::

    # ...
    info['key'] = 20 # access with key
    info.key += 1 # access with attribute
    print info.key # 21

When defining a notification method, e.g. statically with decorator::

    @Observer.observe('prop2', assign=True, signal=True, foo="a-value-for-foo")
    def notifications(self, model, prop_name, info):
        # ...
        return 

Instance :obj:`info` in method notification will contain some of
the keyword arguments and associated values which were specified at
declaration time::

    @Observer.observe('prop2', assign=True, signal=True, foo='a-value-for-foo')
    def notifications(self, model, prop_name, info):
        assert info['assign'] ^ info.signal
        assert 'a-value-for-foo' == info.foo
        return

In particular, in each notification call only *one* of the keyword
arguments identifying the type of the notification is set. All the
other keyword arguments are copied as they are.

Apart from keyword parameters used when declaring the notification
method, :obj:`info` contains also attributes:

   * :attr:`model`: the model containing the OP which was
     changed. This is also passed to the notification method as first
     argument.

   * :attr:`prop_name`: the name of the OP which was
     changed. This is also passed to the notification method as second
     argument.

The standard remaining content of :obj:`info` depends on the
notification type it is passed along to, and it is listed in detail
now.

It is possible to have one method be declared as a notification for
several properties. E.g.::

    @Observer.observe('prop1', assign=True, signal=True, foo1='value1')
    @Observer.observe('prop2', after=True, foo2='value2')
    @Observer.observe('prop3', assign=True, before=True, foo3='value3')
    def notify(self, model, prop_name, info):
        # ...
        return

When invoked, the notification's info parameter will be filled with
data according to each declaration. In the example, only the assign
notification regarding `prop2` will carry key `foo2` in the `info`
parameter.

However, when declaring a method as a notification for a property,
that property cannot be occur in other declarations regarding the same
method::

    @Observer.observe('prop1', assign=True, signal=True, foo1='value1')
    @Observer.observe('prop2', after=True, foo2='value2')
    @Observer.observe('prop2', assign=True, before=True, foo3='value3') #ERROR!
    def notify(self, model, prop_name, info):
        # ...
        return


Notification types
------------------

The type of the notification method is decided at declaration time, by
using specific flags as keyword arguments. Later in the notification
method, parameter :obj:`info` will carry specific information which
depend on the notification type. In the following table details of all
the supported types are presented.

Common to all types
^^^^^^^^^^^^^^^^^^^

.. class:: NTInfo

    .. attribute:: model                              
                                                      
       The model instance containing the OP which     
       has been changed.                                   
                                                      
       :type: `gtkmvc.Model`                          
                                                      
    .. attribute:: prop_name                          
                                                      
       The name of the OP which has beeen changed.    
                                                      
       :type: `string`                                


Assign Type
^^^^^^^^^^^

Keyword argument to be used on `Observer.observe`: `assign=True`

.. class:: NTInfo
                                                     
    .. attribute:: old                               
                                                     
       Holds the value which the property had before 
       being assigned to (i.e. the previous value)   
                                                     
       :type: <any>                                  
                                                     
    .. attribute:: new                               
                                                     
       Holds the value which the property has been   
       assigned to (i.e. the current value)          
                                                     
       :type: <any>                                  

    .. attribute:: spurious
                                                     
       Holds the value of the flag which can be used to change the
       spuriousness of the specific notification method, overriding
       the global spuriousness of the :class:`Observer`. If `True`,
       the notification method will be called when the observable
       property is assigned, also when its value does not change. If
       `False`, spurious notifications will be not sent independently
       on the `spurious` parameter passed to
       :meth:`Observer.__init__`.
                                              
       :type: bool

       .. versionadded:: 1.99.2


Before method call type
^^^^^^^^^^^^^^^^^^^^^^^
Keyword argument to be used on `Observer.observe`: `before = True`


.. class:: NTInfo 
                                                     
    .. attribute:: instance                          
                                                     
       The mutable instance which is being changed.  
                                                     
       :type: <any mutable>                          
                                                     
    .. attribute:: method_name                       
                                                     
       The name of the instance's method which is    
       being called to change the instance.          
                                                     
       :type: `string`                               
                                                     
    .. attribute:: args                              
                                                     
       List of actual arguments passed to the        
       instance's method which is being called.      
                                                     
       :type: `list`                                 
                                                     
    .. attribute:: kwargs                            
                                                     
       Dictionary of the keyword arguments passed to 
       the instance's method which is being called.  
                                                     
       :type: `dict`                                 


After method call type
^^^^^^^^^^^^^^^^^^^^^^
Keyword argument to be used on `Observer.observe`: `after = True` 

This is similar to `before` but features an attribute to carry the
return value of the method.

.. class:: NTInfo 
                                                     
    .. attribute:: instance                          
                                                     
       The mutable instance which has been changed.  
                                                     
       :type: `instance`                             
                                                     
    .. attribute:: method_name                       
                                                     
       The name of the instance's method which has   
       been called to change the instance.           
                                                     
       :type: `string`                               
                                                     
    .. attribute:: args                              
                                                     
       List of actual arguments passed to the        
       instance's method which has been called.      
                                                     
       :type: `list`                                 
                                                     
    .. attribute:: kwargs                            
                                                     
       Dictionary of the keyword arguments passed to 
       the instance's method which has been called.  
                                                     
       :type: `dict`                                 
                                                     
    .. attribute:: result                            
                                                     
       The value returned by the instance's method.  
                                                     
       :type: <any>                                  


Signal emit type
^^^^^^^^^^^^^^^^
Keyword argument to be used on `Observer.observe`: `signal = True` 

.. class:: NTInfo
                                                     
    .. attribute:: arg                               
                                                     
       The optional argument passed to signal's      
       `emit()` method. `arg` is `None` if           
       `emit` was called without argument.           
                                                     
       :type: <any>                                  


Notification methods and Inheritance
------------------------------------

Notification methods behaves exactly like any normal method when
classes are derived. When overriding notification methods in derived
classes, it is not necessary to re-declare them as notification
methods, as any information provided in base classes is retained
untouched in derived classes.

For example::

 from gtkmvc import Observer, Model, Signal

 class MyModel (Model):
     prop1 = Signal()
     __observables__ = ("prop1",)
     pass # end of class BaseObs

 class BaseObs (Observer):
     @Observer.observe("prop1", assign=True, user_data="my-data-in-BaseObs")
     def notification(self, model, name, info):
         print "BaseObs.notification:", model, name, info
         return
     pass # end of class BaseObs

 class DerObs (BaseObs):
     def notification(self, model, name, info):
         print "DerObs.notification:", model, name, info
         return
     pass # end of class BaseObs


 m = MyModel()
 do = DerObs(m)
 m.prop1 = Signal()

The execution of this code will output::

 DerObs.notification: <__main__.MyModel object ..> prop1 
 { 'model': <__main__.MyModel object ...>,
   'prop_name': 'prop1', 
   'assign': True, 
   'old': <gtkmvc.observable.Signal object at 0x12a6110>, 
   'new': <gtkmvc.observable.Signal object at 0x12a64d0>, 
   'user_data': 'my-data-in-BaseObs' }

As you see the actually called method is
meth:`DerObs.notification`, even if the method in
:class:`DerObs` is not explicitly declared to be a notification
method. Furthermore, the keyword arguments specified at declaration
time in class :class:`BaseObs` are passed down to :obj:`info`
untouched.

Sometimes it is useful to re-define notification methods in derived
class. In this case it is sufficient to use again static or dynamic
declaration in derived class. It is important to notice here that when
notifications in derived classes are redefined, notifications in base
classes are hidden. For example::

 from gtkmvc import Observer, Model, Signal

 class MyModel (Model):
     prop1 = Signal()
     __observables__ = ("prop1",)
     pass # end of class BaseObs

 class BaseObs (Observer):
     @Observer.observe("prop1", assign=True, user_data="my-data-in-BaseObs")
     def notification(self, model, name, info):
         print "BaseObs.notification:", model, name, info
         return
     pass # end of class BaseObs

 class DerObs (BaseObs):
     @Observer.observe("prop1", signal=True,
                       user_data="my-data-in-DerObs",
                       other_data="other-data-in-DerObs")
     def notification(self, model, name, info):
         print "DerObs.notification:", model, name, info
         return
     pass # end of class BaseObs


 m = MyModel()
 do = DerObs(m)
 m.prop1 = Signal()
 m.prop1.emit("wake up!")

The execution of this code produces the output::

 DerObs.notification: <__main__.MyModel object ...> prop1 
 { 'model': <__main__.MyModel object ...>, 
   'prop_name': 'prop1', 
   'signal': True, 
   'arg': 'wake up!', 
   'user_data': 'my-data-in-DerObs', 
   'other_data': 'other-data-in-DerObs' }

Notice that even if :obj:`prop1` has been assigned, the *assign*
notification has not been sent, as :meth:`DerObs.notification`
intercepts only *signals* and :meth:`BaseObs.notification` is
shadowed by it.

However, if we declare :meth:`DerObs.notification` to receive both
*assign* and *signal* notifications::

 class DerObs (BaseObs):
     @Observer.observe("prop1", signal=True, assign=True,
                       user_data="my-data-in-DerObs",
                       other_data="other-data-in-DerObs")
     def notification(self, model, name, info):
         print "DerObs.notification:", model, name, info
         return
     pass # end of class BaseObs

The execution produces two notifications as expected::

 DerObs.notification: <__main__.MyModel object ...> prop1 
 { 'model': <__main__.MyModel object ...>, 
   'prop_name': 'prop1', 
   'assign': True, 
   'old': <gtkmvc.observable.Signal object at 0x7fc5098ab110>, 
   'new': <gtkmvc.observable.Signal object at 0x7fc5098ab4d0>, 
   'user_data': 'my-data-in-DerObs',    
   'other_data': 'other-data-in-DerObs' }

 DerObs.notification: <__main__.MyModel object ...> prop1 
 { 'model': <__main__.MyModel object ...>, 
   'prop_name': 'prop1', 
   'signal': True, 
   'arg': 'wake up!', 
   'user_data': 'my-data-in-DerObs', 
   'other_data': 'other-data-in-DerObs' }


Old-style notifications
-----------------------

Naming conventions-based
^^^^^^^^^^^^^^^^^^^^^^^^
Old style notifications (version 1.99.0 and older) were implicitly
declared by exploiting a *naming convention*. :class:`NTInfo` was
not supported, and notification methods had different signatures
depending on the notification type.

For example, an *assign* type notification method for property `prop1`
was defined as::

 def property_prop1_value_change(self, model, old, new): 
     # ...
     return

*after* type notifications were more complicated::

 def property_prop1_after_change(self, model, instance, 
                                 method_name, res, args, kwargs): 
     # ...
     return

If this implicit mechanism is still supported for backward
compatibility, is should be not used anymore in new code, use static
or dynamic declaration mechanisms instead.


Decorator-based
^^^^^^^^^^^^^^^
In release 1.99.0 featured an experimental decorator
`@observer.observes` which could be used for multiple properties
assign-type only notifications::

  @observer.observes ("prop1", "prop2")
  def notification(self, model, name, old, new):
      # ...
      return

This decorator has been fully substituted by `Observer.observe` and
should be not used anymore. However, it is still supported.

