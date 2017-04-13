.. pygtkmvc documentation master file, created by
   sphinx-quickstart on Fri Mar 11 12:35:33 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |gtkmvc| replace:: *gtkmvc*


Welcome to pygtkmvc
====================================

|gtkmvc| is a thin framework for supporting GUI programming with Python and PyGTK. Its major features are:

   #. A practical implementation of a Model-View-Controller pattern dialect.
   #. A transparent implementation of the Observer pattern.
   #. Guides the design and the structure to your application, still being behind the scene.
   #. |gtkmvc| is small: you can distribute it along with your application, with no bad effects on its dependencies list.
   #. A good set of documentation. 

For a quick example, see :doc:`five_min/index`.

|gtkmvc| is often compared to the great project Kiwi.
However, the two projects are different, as Kiwi focuses more on the presentation side while |gtkmvc| is more focused on the logic side of the application, and does not provide any extension to what the toolkit PyGTK provides.


Table of Contents:
------------------

.. toctree::
   :maxdepth: 1

   gettingstarted
   documentation


Motivations
-----------

Programming GUI applications is a terribly plain boring task

Period. As that's a hardly questionable statement, my suggestion is to always consider a batch modality (no GUI) first for the interface of your application. Or at least to consider supporting a batch modality anyhow. In this sense having the logic of the application separated from the presentation layer can largely help.

If GUI programming is not exactly rocket science, it can become even a pain in the neck. In fact GUI handling code (especially the control flow part) tends to blow up linearly in size, and it is inclined to get containing many wrong dependencies.

If there are no barriers among the logic and presentation layers, the well-known laziness of programmers wins the day. The ending result is a spaghetti code which is later very hard to get relieved of.

gtkmvc plays a rule to help designers to correctly structure their applications, and to provide them with a easy, light, non-invasive and still high-level framework which in the end makes GUI programming an easier task. 


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

