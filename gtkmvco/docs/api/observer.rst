Observers
=========

.. module:: gtkmvc.observer

.. autofunction:: observes(*args)

.. autoclass:: Observer
    :members:
    :exclude-members: get_custom_observing_methods
    :undoc-members:

    .. method:: get_custom_observing_methods(prop_name)

       An alias for :meth:`get_observing_methods`.

       .. deprecated:: 1.99.1

.. class:: NTInfo(type, *args, **kwargs)

	A container for information attached to a notification.
	This class is a dictionary-like object used:

	1. As class when defining notification methods in observers, as it
	   contains the flags identifying the notification types.

	2. As class instance as parameter when a notification methods is
	   called in observers.


	**Notification Type Flags**

	Notification methods are declared either statically or dynamically 
	through :meth:`Observer.observe`. In both cases the type of the
	notification is defined by setting to `True` some flags. Flags can
	be set in any combination for multi-type notification
	methods. Flags are:

	assign
	   For notifications issued when OPs are assigned.
	before
	   For notifications called before a modifying method is called.
	after
	   For notifications called after a modifying method is called.
	signal
	   For notifications called when a signal is emitted.


	**Instance content**

	Instances of class `NTInfo` will be received as the last argument
	(`info`) of any notification method::

	  def notification_method(self, model, name, info)

	NTInfo is a dictionary (with some particular behaviour added)
	containing some information which is independent on the
	notification type, and some other information wich depends on the
	notification type.


	**Common to all types**

	For all notification types, NTInfo contains:

	model
	   the model containing the observable property triggering the
	   notification. `model` is also passed as first argument of the
	   notification method.

	prop_name
	   the name of the observable property triggering the notification. `name`
	   is also passed as second argument of the notification method.
  
	Furthermore, any keyword argument not listed here is copied
	without modification into `info`.

	There are further information depending on the specific
	notification type:

	**For Assign-type**

	assign
	   flag set to `True`

	old
	   the value that the observable property had before being
	   changed.

	new
	   the new value that the observable property has been
	   changed to.

	spurious
	   the flag which can be used to change the spuriousness of the
	   specific notification method, overriding the global
	   spuriousness of the :class:`Observer`. If `True`, the
	   notification method will be called when the observable property
	   is assigned, also when its value does not change. If `False`, spurious
	   notifications will be not sent independently on the `spurious`
	   parameter passed to :meth:`Observer.__init__`.

	   .. versionadded:: 1.99.2

	**For Before method call type**

	before
	   flag set to `True`

	instance
	   the object instance which the method that is being called belongs to.

	method_name
	   the name of the method that is being called. 

	args
	   tuple of the arguments of the method that is being called. 

	kwargs
	   dictionary of the keyword arguments of the method that
	   is being called.


	**For After method call type**

	after
	   flag set to `True`

	instance
	   the object instance which the method that has been 
	   called belongs to.

	method_name
	   the name of the method that has been called. 

	args
	   tuple of the arguments of the method that has been called. 

	kwargs
	   dictionary of the keyword arguments of the method that
	   has been called.

	result
	   the value returned by the method which has been called. 

	**For Signal-type**

	signal
	   flag set to `True`

	arg
	   the argument which was optionally specified when invoking
	   emit() on the signal observable property.

	**Information access**

	The information carried by a NTInfo instance passed to a
	notification method can be retrieved using the instance as a
	dictionary, or accessing directly to the information as an
	attribute of the instance. For example::
   
	   # This is a multi-type notification
	   @Observer.observe("op1", assign=True, hello="Ciao")
	   @Observer.observe("op2", after=True, before=True)
	   def notify_me(self, model, name, info):
	       assert info["model"] == model # access as dict key
	       assert info.prop_name == name # access as attribute

	       if "assign" in info:
	          assert info.old == info["old"]
	          assert "hello" in info and "ciao" == info.hello
	          print "Assign from", info.old, "to", info.new
	       else:
	          assert "before" in info or "after" in info
	          assert "hello" not in info
	          print "Method name=", info.method_name
	          if "after" in info: print "Method returned", info.result    
	          pass
          
	       return   

	As already told, the type carried by a NTInfo instance can be
	accessed through boolean flags `assign`, `before`, `after` and
	`signal`. Furthermore, any other information specified at
	declaration time (keyword argument 'hello' in the previous
	example) will be accessible in the corresponding notification
	method.

	.. versionadded:: 1.99.1
