#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2007 by Roberto Cavada
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


import types
import gtk
import time
import new

from gtkmvc.support.utils import cast_value
from gtkmvc.adapters.default import * 
from gtkmvc.observer import Observer
from gtkmvc import Model

class Intermediate(Observer):
    def __init__(self, model, path, adapter):
        """
        *model* is an instance.

        *path* is a list of strings, with the first naming a property of
        *model*. Its value must have a property named like the second string,
        and so on.

        *adapter* is an instance. Its widget will be updated every time a
        property in *path* changes. Currently this only covers assignment.
        """
        self.model = model
        self.prop_name = path[0]
        self.path = path[1:]
        self.adapter = adapter
        self.next = None

        Observer.__init__(self)
        self.observe(self.update_widget, self.prop_name, assign=True)
        self.observe_model(model)

        self.create_next()

    def create_next(self):
        if self.path:
            self.next = Intermediate(
                getattr(self.model, self.prop_name), self.path, self.adapter)

    def delete_next(self):
        if self.next:
            self.next.delete()
            self.next = None

    def delete(self):
        self.relieve_model(self.model)
        self.delete_next()

    def update_widget(self, model, prop_name, info):
        self.delete_next()
        self.create_next()
        model = info.new
        for prop_name in self.path:
            model = getattr(model, prop_name)
        # Break encapsulation to change the model of our adapter.
        self.adapter.relieve_model(model)
        self.adapter._model = model
        self.adapter.observe_model(model)
        self.adapter.update_widget()

# ----------------------------------------------------------------------
class Adapter (Observer):

    def __init__(self, model, prop_name,
                 prop_read=None, prop_write=None, 
                 value_error=None,
                 spurious=False, prop_cast=True):
        """
        Observe one property of one model instance for assignment (and nothing
        else). After you :meth:`connect_widget` those changes will be
        propagated to that widget, and vice versa.
        
        *prop_name* is a string. It may contain dots and will be resolved
        using Python attribute access on *model*. All objects traversed must
        be :class:`Model` instances.
        The last part of the string names a property. Examples::

         >>> "age"
         observe("age")
         observe_model(model)

         >>> "child.age"
         observe("age")
         observe_model(model.child)

        .. versionchanged:: 1.99.2
          Changes to intermediate models used to be ignored.

        *spurious* see superclass.

        *prop_read* is an optional callable. It will be passed the actual
        value of the model property and must return it in a format suitable
        for the widget.
        
        *prop_write* is the mirror image of *prop_read*.
        
        *prop_cast* denotes whether to attempt a cast of the widget value to
        the type of the previous property value, before passing the result to
        *prop_write*. You cannot disable this unless you define *prop_write*.
        
        *value_error* is an optional callable. It is used when the automatic
        cast or *prop_write* raise :exc:`ValueError`. It will be passed this
        adapter, the name of the property we observe (i.e. the last part of
        *prop_name*) and the value obtained from the widget.
        """

        # registration is delayed, as we need to create possible
        # listener before:
        Observer.__init__(self, spurious=spurious)        

        self._prop_name = prop_name
        self._prop_cast = prop_cast
        self._prop_read = prop_read
        self._prop_write = prop_write
        self._value_error = value_error
        self._wid = None
        self._wid_info = {}
        
        # this flag is set when self is changing the property or the
        # widget, in order to avoid infinite looping.
        self._itsme = False 

        self._connect_model(model)
        return

    def get_property_name(self):
        """
        Returns the name of the property we observe.
        """
        return self._prop_name

    def get_widget(self):
        """
        Returns the widget we are connected to, or None.
        """
        return self._wid
    
    def connect_widget(self, wid,
                       getter=None, setter=None, 
                       signal=None, arg=None, update=True,
                       flavour=None):

        """
        Finish set-up by connecting the widget. The model was already
        specified in the constructor.
        
        *wid* is a widget instance.
        
        *getter* is a callable. It is passed *wid* and must return its
        current value.
        
        *setter* is a callable. It is passed *wid* and the current value of
        the model property and must update the widget.
        
        *signal* is a string naming the signal to connect to on *wid*. When
        it is emitted we update the model.
        
        *getter*, *setter* and *signal* are optional. Missing values are
        guessed from *wid* using
        :meth:`gtkmvc.adapters.default.search_adapter_info`. If nothing is
        found this raises :exc:`TypeError`.
        
        *arg* is an optional value passed to the handler for *signal*. This
        doesn't do anything unless a subclass overrides the handler.
        
        *update* denotes whether to update the widget from the model
        immediately. Otherwise the widget stays unchanged until the first
        notification.

        *flavour* can be used to select special behaviours about
         the adaptation when twice or more possibilities are
         possibly handled for the same widget type. See
         adapters.default for further information.

        """

        if self._wid_info.has_key(wid):
            raise ValueError("Widget " + str(wid) + " was already connected")
        
        wid_type = None

        if None in (getter, setter, signal):
            w = search_adapter_info(wid, flavour)
            if getter is None: getter = w[GETTER]
            if setter is None:
                setter = w[SETTER]
                wid_type = w[WIDTYPE]
                pass
            
            if signal is None: signal = w[SIGNAL]
            pass

        # saves information about the widget
        self._wid_info[wid] = (getter, setter, wid_type)

        # connects the widget
        if signal:
            if arg: wid.connect(signal, self._on_wid_changed, arg)
            else: wid.connect(signal, self._on_wid_changed)
            pass

        self._wid = wid

        # updates the widget:
        if update: self.update_widget()
        return
        
    def update_model(self):
        """
        Update the model with the current value from the widget.

        It shouldn't ever be necessary to call this, if you connected to
        the right signal.
        """
        try: val = self._read_widget()
        except ValueError: pass
        else: self._write_property(val)
        return
    
    def update_widget(self):
        """
        Update the widget with the current value from the model.

        Use this for changes to the property that assignment observation
        doesn't catch.
        """
        self._write_widget(self._read_property())
        return


    # ----------------------------------------------------------------------
    #  Private methods
    # ----------------------------------------------------------------------
    def _connect_model(self, model):
        """
        Used internally to connect the property into the model, and
        register self as a value observer for that property"""

        parts = self._prop_name.split(".")
        if len(parts) > 1:
            # identifies the model
            models = parts[:-1]
            Intermediate(model, models, self)
            for name in models:
                model = getattr(model, name)
                if not isinstance(model, Model):
                    raise TypeError("Attribute '" + name +
                                    "' was expected to be a Model, but found: " +
                                    str(model))
                pass
            prop = parts[-1]
        else: prop = parts[0]

        # prop is inside model?
        if not hasattr(model, prop):
            raise ValueError("Attribute '" + prop +
                             "' not found in model " + str(model))

        # is it observable?
        if model.has_property(prop):
            # we need to create an observing method before registering
            meth = new.instancemethod(self._get_observer_fun(prop),
                                      self, self.__class__)
            setattr(self, meth.__name__, meth)
            pass

        self._prop = getattr(model, prop)
        self._prop_name = prop
        
        # registration of model:
        self._model = model
        self.observe_model(model)
        return
    
    def _get_observer_fun(self, prop_name):
        """This is the code for an value change observer"""
        def _observer_fun(self, model, old, new):
            if self._itsme: return
            self._on_prop_changed()
            return
        
        # doesn't affect stack traces
        _observer_fun.__name__ = "property_%s_value_change" % prop_name
        return _observer_fun

    def _get_property(self):
        """Private method that returns the value currently stored
        into the property"""
        return getattr(self._model, self._prop_name)
        #return self._prop # bug fix reported by A. Dentella

    def _set_property(self, val):
        """Private method that sets the value currently of the property."""
        return setattr(self._model, self._prop_name, val)

    def _read_property(self, *args):
        """
        Return the model's current value, using *prop_read* if used in the
        constructor.
        
        *args* is just passed on to :meth:`_get_property`. This does nothing,
        but may be used in subclasses.
        """
        if self._prop_read: return self._prop_read(self._get_property(*args))
        return self._get_property(*args)

    def _write_property(self, val, *args):
        """Sets the value of property. Given val is transformed
        accodingly to prop_write function when specified at
        construction-time. A try to cast the value to the property
        type is given."""
        val_wid = val
        # 'finally' would be better here, but not supported in 2.4 :(
        try: 
            totype = type(self._get_property(*args))

            if totype is not types.NoneType and (self._prop_cast or not self._prop_write):
                val = self._cast_value(val, totype)
            if self._prop_write: val = self._prop_write(val)

            self._itsme = True
            self._set_property(val, *args)

        except ValueError:
            self._itsme = False
            if self._value_error: self._value_error(self, self._prop_name, val_wid)
            else: raise
            pass

        except: self._itsme = False; raise

        self._itsme = False
        return

    def _read_widget(self):
        """Returns the value currently stored into the widget, after
        transforming it accordingly to possibly specified function.

        This is implemented by calling the getter provided by the
        user. This method can raise InvalidValue (raised by the
        getter) when the value in the widget must not be considered as
        valid."""
        getter = self._wid_info[self._wid][0]
        return getter(self._wid)
        
    def _write_widget(self, val):
        """Writes value into the widget. If specified, user setter
        is invoked."""
        self._itsme = True
        try:
            setter = self._wid_info[self._wid][1]
            wtype = self._wid_info[self._wid][2]
            if setter:
                if wtype is not None: setter(self._wid, self._cast_value(val, wtype))
                else: setter(self._wid, val)
                pass
        finally:
            self._itsme = False
            pass
        
        return
         
    def _cast_value(self, val, totype):
        return cast_value(val, totype)


    # ----------------------------------------------------------------------
    # Callbacks and observation
    # ----------------------------------------------------------------------

    def _on_wid_changed(self, wid, *args):
        """Called when the widget is changed"""
        if self._itsme: return
        self.update_model()
        return

    def _on_prop_changed(self):
        """Called by the observation code, when the value in the
        observed property is changed"""
        if self._wid and not self._itsme: self.update_widget()
        return

    pass # end of class Adapter



#----------------------------------------------------------------------
class UserClassAdapter (Adapter):
    """
    This class handles the communication between a widget and a
    class instance (possibly observable) that is a property inside
    the model. The value to be shown is taken and stored by using a
    getter and a setter. getter and setter can be: names of user
    class methods, bound or unbound methods of the user class, or a
    function that will receive the user class instance and possible
    arguments whose number depends on whether it is a getter or a
    setter."""
    
    def __init__(self, model, prop_name,
                 getter, setter, 
                 prop_read=None, prop_write=None,                   
                 value_error=None, spurious=False):

        Adapter.__init__(self, model, prop_name,
                         prop_read, prop_write, value_error,
                         spurious)

        self._getter = self._resolve_to_func(getter)
        self._setter = self._resolve_to_func(setter)
        return

    # ----------------------------------------------------------------------
    # Private methods 
    # ----------------------------------------------------------------------

    def _resolve_to_func(self, what):
        """This method resolves whatever is passed: a string, a
        bound or unbound method, a function, to make it a
        function. This makes internal handling of setter and getter
        uniform and easier."""
        if isinstance(what, types.StringType):
            what = getattr(Adapter._get_property(self), what)
            pass

        # makes it an unbounded function if needed
        if type(what) == types.MethodType: what = what.im_func

        if not type(what) == types.FunctionType: raise TypeError("Expected a method name, a method or a function")
        return what
    

    def _get_observer_fun(self, prop_name):
        def _observer_fun(self, model, instance, meth_name, res, args, kwargs):
            if self._itsme: return
            self._on_prop_changed(instance, meth_name, res, args, kwargs)
            return

        _observer_fun.__name__ = "property_%s_after_change" % prop_name
        return _observer_fun
    
    def _on_prop_changed(self, instance, meth_name, res, args, kwargs):
        """Called by the observation code, when a modifying method
        is called"""
        Adapter._on_prop_changed(self)
        return

    def _get_property(self, *args):
        """Private method that returns the value currently stored
        into the property"""
        val = self._getter(Adapter._get_property(self), *args)
        if self._prop_read: return self._prop_read(val, *args)
        return val

    def _set_property(self, val, *args):
        """Private method that sets the value currently of the property"""
        if self._prop_write: val = self._prop_write(val)
        return self._setter(Adapter._get_property(self), val, *args)
    
    pass # end of class UserClassAdapter
# ----------------------------------------------------------------------



#----------------------------------------------------------------------
class RoUserClassAdapter (UserClassAdapter):
    """
    This class is for Read-Only user classes. RO classes are those
    whose setting methods do not change the instance, but return a
    new instance that has been changed accordingly to the setters
    semantics. An example is python datetime class, whose replace
    method does not change the instance it is invoked on, but
    returns a new datetime instance.

    This class is likely to be used very rarely. 
    """
    
    def __init__(self, model, prop_name,
                 getter, setter, 
                 prop_read=None, prop_write=None,                   
                 value_error=None, spurious=False):

        UserClassAdapter.__init__(self, model, prop_name,
                                  getter, setter,
                                  prop_read, prop_write, value_error,
                                  spurious)

        return

    # ----------------------------------------------------------------------
    # Private methods 
    # ----------------------------------------------------------------------
    def _get_observer_fun(self, prop_name):
        """Restore Adapter's behaviour to make possible to receive
        value change notifications"""
        return Adapter._get_observer_fun(self, prop_name)
    
    def _on_prop_changed(self):
        """Again to restore behaviour of Adapter"""
        return Adapter._on_prop_changed(self)

    def _set_property(self, val, *args):
        """Private method that sets the value currently of the property"""
        val = UserClassAdapter._set_property(self, val, *args)
        if val: Adapter._set_property(self, val, *args)
        return val

    pass # end of class RoUserClassAdapter
# ----------------------------------------------------------------------
