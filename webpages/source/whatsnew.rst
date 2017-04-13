.. include:: common.rst 

.. _what_is_new:

===========
What's new?
===========

.. figure:: _static/gift_surprise.jpg
   :width: 5cm
   :align: right


.. _rel_1.99.1:

Version 1.99.1
--------------

(December 2010)

This is a release that keeps compatibility with previous version
:ref:`1.99.0 <rel_1.99.0>`. However, some features provided in 1.99.0
are deprecated in 1.99.1.

This version goes in the direction of stabilizing the API and making
the code more robust. Many bugs were fixed, and a new, clean API is
now provided for defining notification methods in observers, and
logical observable properties in models.

The documentation has been updated and extended to reflect all
changes, and a complete Library Reference is now
available. Furthermore, the documentation now uses `Sphinx
<http://sphinx.pocoo.org/>`_ instead of Latex to generate both pdf and
html documentation formats.

Last but not the least, the team grew up!

New
~~~

* Models now feature Logical Observable Properties, along with
  already supported Concrete Observable Properties.

* In Observers notification methods have all the same prototype,
  which make much cleaner the application code.

* New mechanism to declare both dynamically and statically
  notification methods in Observers.

* Auto-adapt of `gtk.FileChooserButton`, `gtk.ComboBox` and
  `gtk.Adjustment`.

* API to extend default adapter list.

* More widget types now correctly cast when adapted to
  unicode/int/float properties.

* Enable `gtkmvc.RoUserClassAdapter` to update the widget. It used to
  only do it when connecting, not on property changes. This makes the
  built-in support for gtk.Calendar work in both directions.

* Controller's method adapt() allows auto-adaption even if the
  view does not have corresponding widgets for *all* properties in
  the model.

* Adapters can optionally call prop_write *instead of* casting the
  value from the widget to the type of the old property
  value. This was the intended behaviour all along. Default is
  still to call it after the cast.

* Decorators for property setters/getters in models. The methods
  can now have arbitrary names and you are no longer limited to
  one property per method.

Changed
~~~~~~~

* Name-based notification methods like `property_<name>_value_change`
  are still supported, but their usage is now *discouraged*. A new
  mechanism for declaring notifications is now available, and you
  should consider porting applications accordingly.

* Decorator `Observer.observes` is now *deprecated*. A new mechanism for
  declaring notifications is now available, and you should consider
  porting applications accordingly.

* Support `gtk.Builder` in addition to `libglade`, which is no longer
  required. This changed the signature of the `gtkmvc.View`
  constructor. The two formats are not equivalent, as GTK cannot build
  only parts of a file.

* Allow creation of adapters that act on spurious notifications.

* Use no eval(codestring) This changed how adapters create observer
  functions. If you have adapter subclasses you will have to adjust
  them.

* Misuse of the framework that used to exit your application can now
  be caught as exceptions.

* Fewer warnings printed by the framework. Remember to increase the
  logging level during development.


Fixed
~~~~~

* Assigning a tuple with length 3 to a property no longer raises

* Pass the correct model when emitting notifications for an inherited
  signal. This changes how all property wrappers track their owners,
  but your code should not be affected.

* Wrapped sequences lacked crucial special methods like len and iter.

* Inspecting wrappers no longer omits the class name. 

* Various changes to make `SQLObjectModel` actually usable.

* Wrapping more than one sequence class could cause the wrong methods
  to be called on all but the last instance created. This did not
  affect programs that only use the built-in list type.

* Mutable instances that used to be assigned to properties would
  notify of their changes even after being replaced in the model.

* No more errors from static container adapters you didn't create.

* Multiple concurrent iterators on views no longer steal each other
  widgets.


.. _rel_1.99.0:

Version 1.99.0
--------------

|pygtkmvc| has been around for some years. There were several limits
in 1.x family that have been faced in the last months thanks to user's
feedback, requests and critics.

This new version is the first result of a massive effort for improving
it. It is marked as 1.99 as it is no backward compatible with previous
stable versions, and at the same time there might be a few changes in
the forthcoming weeks that make it not stable yet.

1. Controllers decomposition 

    There are several new features, and others are still under
    development, but one single feature breaks the backward
    compatibility:

    **the view constructor no longer takes a controller, and the
    controller constructor takes the view together with the model.**

    I realized recently that what I initially thought was mainly a
    design fix, it is actually the most important feature. Because now
    there is a *natural* way for decomposing controllers.

    Now that a view can have several controllers, it is possible in
    fact to have the view separated into partitions, and what before
    was a big controller split into several controllers each
    controlling one part of the shared view.

2. Compatibility with `SQLObject <http://www.sqlobject.org/>`_

    Even if still experimental, now |pygtkmvc| is compatible with
    SQLObject. Next releases will provide also support for 
    `SQLAlchemy <http://www.sqlalchemy.org/>`_

3. Models support non-locally stored observable properties 

    It i now possible to define special methods to get/set values of
    observable properties that do not live into the model. For example
    values may reside into a DB, a file or on the network.

4. Observers can define explicit observing methods 

    Instead of using naming conventions, it is possible to explicitly
    define methods that are intended to receive notifications from
    observable properties. Definition is made through very readable
    decorators.

5. New documentation: new website, new quickstart guide 

6. Customizable logging system for debugging, warnings and errors 

7. Some bug fixes and changes that improve performances and
   readability
