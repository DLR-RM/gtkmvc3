#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2005 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


from gtkmvc.observer import Observer
from gtkmvc.support.log import logger
from gtkmvc.support.utils import cast_value
from gtkmvc.support.exceptions import TooManyCandidatesError
from gtkmvc.adapters.basic import Adapter, RoUserClassAdapter
from gtkmvc.adapters.containers import StaticContainerAdapter

import types
import gobject
import gtk
import sys

def partition(string, sep):
    """
    New in Python 2.5 as str.partition(sep)
    """
    p = string.split(sep, 1)
    if len(p) == 2:
        return p[0], sep, p[1]
    return string, '', ''

def setup_column(widget, column=0, attribute=None, renderer=None,
    property=None, from_python=None, to_python=None, model=None):
    if not attribute:
        attribute = widget.get_name()
        if attribute is None:
            raise TypeError("Column not named")
    if not renderer:
        renderer = widget.get_cell_renderers()[0]
    if not property:
        for cls, name in [
            (gtk.CellRendererText, 'text'),
            (gtk.CellRendererProgress, 'value'),
            (gtk.CellRendererToggle, 'active'),
            ]:
            if isinstance(renderer, cls):
                property = name
                break
    if not from_python:
        from_python = {
            'text': unicode,
            'value': int,
            'active': bool,
            }.get(property)
    data_func = lambda widget, renderer, model, iter: renderer.set_property(
            property,
            from_python(
                getattr(
                    model.get_value(iter, column),
                    attribute
                    )
                )
            )
    widget.set_cell_data_func(renderer, data_func)
    if not model:
        return
    def callback(renderer, path, new=None):
        try:
            # Function works with bot Text and Toggle.
            new = not renderer.get_active()
        except AttributeError:
            pass
        o = model.get_value(model.get_iter(path), column)
        if to_python:
            new = to_python(new)
        else:
            old = getattr(o, attribute)
            if old is not None:
                new = cast_value(new, type(old))
        setattr(o, attribute, new)
    if isinstance(renderer, gtk.CellRendererText):
        return renderer.connect('edited', callback)
    elif isinstance(renderer, gtk.CellRendererToggle):
        return renderer.connect('toggled', callback)

class Controller (Observer):
    handlers = "glade"

    def __init__(self, model, view, spurious=False, auto_adapt=False,
        handlers=""):
        """
        Two positional and three optional keyword arguments.
        
        *model* will have the new instance registered as an observer.
        It is made available as an attribute.
        
        *view* may contain signal connections loaded from XML. The handler
        methods have to exist in this class.
        
        *spurious* denotes whether notifications in this class will be called
        if a property of *model* is set to the same value it already has.
        
        *auto_adapt* denotes whether to call :meth:`adapt` with no arguments
        as part of the view registration process.

        *handlers* denotes where signal connections are made. Possible values
        are "glade" (the default) and "class". In the latter case all
        controller methods with a name like `on_<widget>__<signal>` (e.g.
        :meth:`on_my_window__delete_event`, note the two underscores) are
        connected automatically.

        View registration consists of connecting signal handlers,
        :meth:`register_view` and :meth:`register_adapters`, and is scheduled
        with the GTK main loop. It happens as soon as possible but after the
        constructor returns. When it starts *view* is available as an
        attribute.
        """
        # In 1.99.0 the third parameter was optional. Now the interpreter will
        # raise if it isn't given.
        if view in (True, False):
            raise NotImplementedError("This version of GTKMVC does not"
                " support the 1.2 API")

        Observer.__init__(self, model, spurious)

        self.handlers = handlers or self.handlers
        self.model = model
        self.view = None
        self.__adapters = []
        # set of properties explicitly adapted by the user:
        self.__user_props = set()
        self.__auto_adapt = auto_adapt
        
        gobject.idle_add(self._idle_register_view, view, priority=gobject.PRIORITY_HIGH)
        return

    def _idle_register_view(self, view):
        """Internal method that calls register_view"""
        assert(self.view is None)
        self.view = view

        if self.handlers == "class":
            for name in dir(self):
                when, _, what = partition(name, '_')
                widget, _, signal = partition(what, '__')
                if when == "on":
                    try:
                        view[widget].connect(signal, getattr(self, name))
                    except IndexError:
                        # Not a handler
                        pass
                    except KeyError:
                        logger.warn("Widget not found for handler: %s", name)
        elif self.handlers == "glade":
            self.__autoconnect_signals()
        else:
            raise NotImplementedError("%s is not a valid source of signal "
                "connections" % self.handlers)

        self.register_view(view)
        self.register_adapters()
        if self.__auto_adapt: self.adapt()
        return False

    def register_view(self, view):
        """
        This does nothing. Subclasses can override it to connect signals
        manually or modify widgets loaded from XML, like adding columns to a
        TreeView. No super call necessary.
        
        *view* is a shortcut for ``self.view``.
        """
        assert(self.model is not None)
        assert(self.view is not None)
        return

    def register_adapters(self):
        """
        This does nothing. Subclasses can override it to create adapters.
        No super call necessary.
        """
        assert(self.model is not None)
        assert(self.view is not None)
        return

    def setup_columns(self):
        """
        Search the view for :class:`TreeView` instances and call
        :meth:`setup_column` on all their columns.

        .. note::
           This is a convenience function. It is never called by the framework.
           You are free to repurpose it in subclasses.

        For editing to work, the widget must already be connected to a model.
        If you don't use :class:`ListStoreModel` this can be done in Glade,
        however a `bug <https://bugzilla.gnome.org/show_bug.cgi?id=597095>`_
        makes versions prior to 3.7.0 (released March 10th, 2010) remove
        Python columns on save. If you want to correct the XML manually, it
        should look like this::

         <object class="GtkListStore" id="liststore1">
           <columns>
             <column type="PyObject"/>
           </columns>
         </object>
        """
        for name in self.view:
            w = self.view[name]
            if isinstance(w, gtk.TreeView):
                m = w.get_model()
                for c in w.get_columns():
                    self.setup_column(c, model=m)

    def setup_column(self, widget, column=0, attribute=None, renderer=None,
        property=None, from_python=None, to_python=None, model=None):
        # Maybe this is too overloaded.
        """
        Set up a :class:`TreeView` to display attributes of Python objects
        stored in its :class:`TreeModel`.

        This assumes that :class:`TreeViewColumn` instances have already
        been added and :class:`CellRenderer` instances packed into them.
        Both can be done in Glade.

        *model* is the instance displayed by the widget. You only need to pass
        this if you set *renderer* to be editable.
        If you use sorting or filtering this may not be the actual data store,
        but all tree paths and column indexes are relative to this.
        Defaults to our model.

        *widget* is a column, or a string naming one in our view.

        *column* is an integer addressing the column in *model* that holds your
        objects.

        *attribute* is a string naming an object attribute to display. Defaults
        to the name of *widget*.

        *renderer* defaults to the first one found in *widget*.

        *property* is a string naming the property of *renderer* to set. If not
        given this is guessed based on the type of *renderer*.

        *from_python* is a callable. It gets passed a value from the object and
        must return it in a format suitable for *renderer*. If not given this
        is guessed based on *property*.

        *to_python* is a callable. It gets passed a value from *renderer* and
        must return it in a format suitable for the attribute. If not given a
        cast to the type of the previous attribute value is attempted.

        If you need more flexibility, like setting multiple properties, setting
        your own cell data function will override the internal one.

        Returns an integer you can use to disconnect the internal editing
        callback from *renderer*, or None.

        .. versionadded:: 1.99.2
        """
        if isinstance(widget, types.StringType):
            widget = self.view[widget]
        if not model and isinstance(self.model, gtk.TreeModel):
            model = self.model
        return setup_column(widget, column=column, attribute=attribute,
            renderer=renderer, property=property, from_python=from_python,
            to_python=to_python, model=model)

    def adapt(self, *args, **kwargs):
        """
        There are five ways to call this:

        .. method:: adapt()
           :noindex:

           Take properties from the model for which ``adapt`` has not yet been
           called, match them to the view by name, and create adapters fitting
           for the respective widget type.

           That information comes from :mod:`gtkmvc.adapters.default`.
           See :meth:`_find_widget_match` for name patterns.

           .. versionchanged:: 1.99.1
              Allow incomplete auto-adaption, meaning properties for which no
              widget is found.

        .. method:: adapt(ad)
           :noindex:

           Keep track of manually created adapters for future ``adapt()``
           calls.

           *ad* is an adapter instance already connected to a widget.

        .. method:: adapt(prop_name)
           :noindex:

           Like ``adapt()`` for a single property.

           *prop_name* is a string.

        .. method:: adapt(prop_name, wid_name)
           :noindex:

           Like ``adapt(prop_name)`` but without widget name matching.

           *wid_name* has to exist in the view.

        .. method:: adapt(prop_name, wid_name, gprop_name)
           :noindex:

           Like ``adapt(prop_name, wid_name)`` but without using default
           adapters. This is useful to adapt secondary properties like
           button sensitivity.

           *gprop_name* is a string naming a property of the widget. No cast
           is attempted, so *prop_name* must match its type exactly.

           .. versionadded:: 1.99.2

        In all cases, optional keyword argument ``flavour=value``
        can be used to specify a particular flavour from those
        available in :mod:`gtkmvc.adapters.default` adapters.
        """

        # checks arguments
        n = len(args)

        flavour = kwargs.get("flavour", None)

        if n==0:
            adapters = []
            props = self.model.get_properties()
            # matches all properties not previoulsy adapter by the user:
            for prop_name in filter(lambda p: p not in self.__user_props, props):
                try: wid_name = self._find_widget_match(prop_name)
                except TooManyCandidatesError, e:
                    # multiple candidates, gives up
                    raise e
                except ValueError, e: 
                    # no widgets found for given property, continue after emitting a warning
                    if e.args:
                        logger.warn(e[0])
                    else:
                        logger.warn("No widget candidates match property '%s'"
                            % prop_name)
                else:
                    logger.debug("Auto-adapting property %s and widget %s" % \
                                     (prop_name, wid_name))
                    adapters += self.__create_adapters__(prop_name, wid_name, flavour)
                    pass
                pass

        elif n == 1: #one argument
            if isinstance(args[0], Adapter): adapters = (args[0],)

            elif isinstance(args[0], types.StringType):
                prop_name = args[0]
                wid_name = self._find_widget_match(prop_name)
                adapters = self.__create_adapters__(prop_name, wid_name, flavour)
                pass
            else: raise TypeError("Argument of adapt() must be either an Adapter or a string")

        elif n == 2: # two arguments
            if not (isinstance(args[0], types.StringType) and
                    isinstance(args[1], types.StringType)):
                raise TypeError("Arguments of adapt() must be two strings")

            # retrieves both property and widget, and creates an adapter
            prop_name, wid_name = args
            adapters = self.__create_adapters__(prop_name, wid_name, flavour)
            pass

        elif n == 3:
            for arg in args:
                if not isinstance(arg, str):
                    raise TypeError("names must be strings")

            prop_name, wid_name, gprop_name = args
            ad = Adapter(self.model, prop_name)
            ad.connect_widget(self.view[wid_name],
                              getter=lambda w: w.get_property(gprop_name),
                              setter=lambda w, v: w.set_property(gprop_name, v),
                              signal='notify::%s' % gprop_name,
                              flavour=flavour)
            adapters = [ad]
            pass

        else:
            raise TypeError(
                "adapt() takes at most three arguments (%i given)" % n)

        for ad in adapters:
            self.__adapters.append(ad)
            # remember properties added by the user
            if n > 0: self.__user_props.add(ad.get_property_name())
            pass
        
        return

    def _find_widget_match(self, prop_name):
        """
        Used to search ``self.view`` when :meth:`adapt` is not given a widget 
        name.
        
        *prop_name* is the name of a property in the model.
        
        Returns a string with the best match. Raises
        :class:`TooManyCandidatesError` or ``ValueError`` when nothing is
        found.

        Subclasses can customise this. No super call necessary. The default
        implementation converts *prop_name* to lower case and allows prefixes
        like ``entry_``.
        """
        names = []
        for wid_name in self.view:
            # if widget names ends with given property name: we skip
            # any prefix in widget name
            if wid_name.lower().endswith(prop_name.lower()): names.append(wid_name)
            pass

        if len(names) == 0:
            raise ValueError("No widget candidates match property '%s': %s" % \
                                 (prop_name, names))

        if len(names) > 1:
            raise TooManyCandidatesError("%d widget candidates match property '%s': %s" % \
                                             (len(names), prop_name, names))
        
        return names[0]

        
    # performs Controller's signals auto-connection:
    def __autoconnect_signals(self):
        """This is called during view registration, to autoconnect
        signals in glade file with methods within the controller"""
        dic = {}
        for name in dir(self):
            method = getattr(self, name)
            if (not callable(method)): continue
            assert(not dic.has_key(name)) # not already connected!
            dic[name] = method
            pass

        # autoconnects glade in the view (if available any)
        for xml in self.view.glade_xmlWidgets: xml.signal_autoconnect(dic)

        # autoconnects builder if available
        if self.view._builder is not None:
            #It was: #self.view._builder.connect_signals(dic)
            self.view._builder_connect_signals(dic)
            pass
        
        return

    
    def __create_adapters__(self, prop_name, wid_name, flavour=None):
        """
        Private service that looks at property and widgets types,
        and possibly creates one or more (best) fitting adapters
        that are returned as a list.

        ``flavour`` is optionally used when a particular flavour
        must be used when seraching in default adapters.
        """
        res = []

        wid = self.view[wid_name]
        if wid is None: raise ValueError("Widget '%s' not found" % wid_name)

        # Decides the type of adapters to be created.
        if isinstance(wid, gtk.Calendar):
            # calendar creates three adapter for year, month and day
            ad = RoUserClassAdapter(self.model, prop_name,
                                    lambda d: d.year,
                                    lambda d,y: d.replace(year=y),
                                    spurious=self.accepts_spurious_change())
            ad.connect_widget(wid, lambda c: c.get_date()[0],
                              lambda c,y: c.select_month(c.get_date()[1], y),
                              "day-selected", flavour=flavour)
            res.append(ad) # year

            ad = RoUserClassAdapter(self.model, prop_name,
                                    lambda d: d.month,
                                    lambda d,m: d.replace(month=m),
                                    spurious=self.accepts_spurious_change())
            ad.connect_widget(wid, lambda c: c.get_date()[1]+1,
                              lambda c,m: c.select_month(m-1, c.get_date()[0]),
                              "day-selected", flavour=flavour)
            res.append(ad) # month

            ad = RoUserClassAdapter(self.model, prop_name,
                                    lambda d: d.day,
                                    lambda d,v: d.replace(day=v),
                                    spurious=self.accepts_spurious_change())
            ad.connect_widget(wid, lambda c: c.get_date()[2],
                              lambda c,d: c.select_day(d),
                              "day-selected", flavour=flavour)
            res.append(ad) # day
            return res

        try: # tries with StaticContainerAdapter
            if "." in prop_name:
                raise TypeError
            ad = StaticContainerAdapter(self.model, prop_name,
                                        spurious=self.accepts_spurious_change())
            ad.connect_widget(wid, flavours=flavour)
            res.append(ad)

        except TypeError, e:
            # falls back to a simple adapter
            ad = Adapter(self.model, prop_name,
                         spurious=self.accepts_spurious_change())
            ad.connect_widget(wid, flavour=flavour)
            res.append(ad)
            pass

        return res


    pass # end of class Controller
