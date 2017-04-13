Implementation of the MVC pattern
=================================

The implementation of the *MVC* pattern provided by *gtkmvc* is a dialect
version of the "official" pattern generally described by Software
Engineering Theory [#theory]_.

.. _MVC_f:

.. figure:: images/mvc.png
   :width: 8 cm
   :align: center

   Simplified Model-View-Controller Pattern

The implementation is different as the view side cannot see the model
part. The reasons behind this difference will be explained later, but
we can anticipate here that this is due to the relationship between
the view and the controller, that is stronger in *gtkmvc* than in the
classic *MVC* pattern. To a certin extend, in *gtkmvc* the view and the
controller parts are separate but could be considered as a unique
entity. However, a view can have multiple controllers (or a single
controller decomposed into many sub-controllers for the sake of
semplicity).


Figure :ref:`MVC_f` shows three interconnected parts:

Model
   Contains the *state* (the *logic*) of the
   application. Also it provides support to access and modify the
   state, and knows how to handle dependencies between different parts
   in the state. For example the application logic could require that
   changing a variable, causes a changing of another. It is not
   required the model user to be aware about this dependency, because
   model autonomously handles it.
 
   Zero, one or more *Controllers* can be connected to one Model
   (see *Controller*, below). Furthermore, one or more
   *Views* can be associated with parts of the state; for example
   a numerical variable could be visualized as a number, as well as a
   graphic bar. It is important to remark that *a Model does not
   know that a set of Views is possibly connected to its state
   through a set of Controllers*.
 
View
   Shows parts of the Model state, and interactively
   exchanges information with the User, via input/output devices.
   A view can be dcomposed into sub-views to simplify the design and
   the reuse. 

   A View collects a set of widget trees built from a *Glade* or
   *gtk.Builder* file, and/or constructed by hand. Since a Widget
   contains a *state*, this implementation differs from the standard
   *MVC* pattern, where generally the View side is completely
   *stateless*.
 
   The View also interacts with zero, one or more *Controllers*
   (see below), sending to it signals, and receiving information to
   visualize.
 
   A View does not know the semantics concerning what it visualizes,
   and neither knows that it is possibly connected to a set of
   controllers.
 
Controller
   Realizes the connection between Models and Views.
   A Controller contains the *GUI* logic: for example, it stores the
   information about what happens when a button is clicked (e.g. 
   handlers of signal are located inside a Controller.)
 
   A Controller perfectly knows the interfaces of the connected Model
   and View, and knows both the state and presentation (*GUI*)
   semantics. A Controller is associated to one Model, and to one
   View, however the Model and the View can be associated to multiple
   controllers. 

   Controllers tend to grow in size, however they can be decomposed
   into sub-controllers, each controlling a subset of the View or the
   Model.


Two particular mechanisms make the isolation between Model and
Controller, and between View and Controller. To support the former,
the *Observer* pattern is provided (see :doc:`obs`), whereas latter mechanism is
provided by the *MVC* pattern, and that is explained in :ref:`VR`.


.. _VR:

View Registration
^^^^^^^^^^^^^^^^^

Current implementation allows a N-1 relationship between Controller
and View. More clearly, one view can have multiple controllers
associated to it, meaning that a View can be shared among several
Controllers. A typical design for large views and controllers makes a
View be split into sets (not necessarily partitions) and each set is
controller by a sub-controller.

After a model and a view have been instantiated (model and view are
*independent*), a controller can be constructed by passing them.

From there on, the Controller can access to the model and the view
state (the set of contained widgets). When the view registers itself
within a Controller, all signals are also automatically connected to
the corresponding methods inside the Controller. Connection in this
case is performed by means of an implicit syntax rule, which binds a
signal name to a corresponding method name.  

This automatic connection can be done either by following the `glade`
or `GtkBuilder` specification, or by following a naming convention.

In sections :ref:`VR:D` and :ref:`VR:EX` more details and an example are
presented, to show how the View registration mechanism can be
exploited by controllers to connect signals and handle the creation of
particular widgets like for example TreeViews, TreeColumns,
CellRenderers, etc.

.. [#theory] For example, see http://www.mimuw.edu.pl/~sl/teaching/00_01/Delfin_EC/Overviews/MVC.htm
