.. include:: common.rst 

=====================
Welcome to |pygtkmvc|
=====================

|pygtkmvc| is a thin Framework for supporting GUI programming with
Python and Pygtk. Its major features are:

1. A practical implementation of a Model-View-Controller pattern dialect.

2. A transparent implementation of the Observer pattern.

3. Guides the design and the structure to your application, still
   being behind the scene.

4. |pygtkmvc| is small: you can distribute it along with your
   application, with no bad effects on its dependencies list.

5. A good :ref:`documentation` set. 

For a quick example, see |pygtkmvc| in 5 minutes.

|pygtkmvc| is often compared to the great project
`Kiwi <http://www.async.com.br/projects/kiwi/>`_. However, the two
projects are different, as Kiwi focuses more on the presentation side
while |pygtkmvc| is more focused on the logic side of the application, and
does not provide any extension to what the toolkit pygtk provides.

|pygtkmvc| is hosted by `SourceForge <http://http://sourceforge.net/projects/pygtkmvc>`_.


News
----

December 30 2010 
         |pygtkmvc| version 1.99.1 has been released!

For all information see :ref:`What's new<what_is_new>`. 


Motivations
-----------

.. figure:: _static/spaghetti_code.jpg
   :width: 8cm
   :align: right


Programming GUI applications is a terribly plain boring task

Period. As that's a hardly questionable statement, my suggestion is to
always consider a batch modality (no GUI) first for the interface of
your application. Or at least to consider supporting a batch modality
anyhow. In this sense having the logic of the application separated
from the presentation layer can largely help.

If GUI programming is not exactly rocket science, it can become even a
pain in the neck. In fact GUI handling code (especially the control
flow part) tends to blow up linearly in size, and it is inclined to
get containing many wrong dependencies.

If there are no barriers among the logic and presentation layers, the
well-known laziness of programmers wins the day. The ending result is
a spaghetti code which is later very hard to get relieved of.

|pygtkmvc| plays a rule to help designers to correctly structure their
applications, and to provide them with a easy, light, non-invasive and
still high-level framework which in the end makes GUI programming an
easier task.


Download
--------

Download of the source code, examples and documentation can be done
`here <http://sourceforge.net/projects/pygtkmvc/files>`_.

Other information can be found in the `SourceForge Project Page
<http://http://sourceforge.net/projects/pygtkmvc>`_.


License
-------

|pygtkmvc| is Free Software, covered by the 
`GNU Lesser General Public License (LGPL) <http://www.gnu.org/licenses/lgpl.html>`_

.. _top_contacts:

Contacts
--------

* For feedback and critics, please post messages to the project
  `mailing list <http://sourceforge.net/mail/?group_id=123428>`_.

* To submit a bug report or to request a new feature, use the
  `project tracker <http://apps.sourceforge.net/trac/pygtkmvc/report/1>`_.
