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
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.

import gtk
import inspect
import types 

import support.metaclasses
from support.wrappers import ObsWrapperBase
from observer import Observer, NTInfo
from observable import Signal
from support.log import logger
from support import decorators
from support.utils import getmembers

# Pass prop_name to this method?
WITH_NAME = True
WITHOUT_NAME = False

def count_leaves(x):
    """
    Return the number of non-sequence items in a given recursive sequence.
    """
    if hasattr(x, 'keys'):
        x = x.values()
    if hasattr(x, '__getitem__'):
        return sum(map(count_leaves, x))
    return 1

class Model (Observer):
    """
    .. attribute:: __observables__
    
       Class attribute. A list or tuple of name strings. The metaclass
       :class:`~gtkmvc.support.metaclasses.ObservablePropertyMeta`
       uses it to create properties.
       
       *Value properties* have to exist as an attribute with an
       initial value, which may be ``None``.

       *Logical properties* require a getter and may have a setter method in
       the class.
    """

    __metaclass__ = support.metaclasses.ObservablePropertyMeta 
    __properties__ = {}  # override this

    # these classes are used internally and by metaclass only
    class __setinfo: 
        def __init__(self, func, has_args): 
            self.func = func
            self.has_args = has_args
            return
        pass
    
    class __getinfo:
        def __init__(self, func, has_args, deps=()): 
            self.func = func
            self.has_args = has_args
            self.deps = deps
            return
        pass

    @classmethod
    @decorators.good_decorator_accepting_args
    def getter(cls, *args, **kwargs):
        """
        Decorate a method as a logical property getter. Comes in two flavours:

        .. method:: getter([deps=(name,...)])
           :noindex:
           
           Uses the name of the method as the property name.
           The method must not require arguments.

        .. method:: getter(one, two, ..., [deps=(name,...)])
           :noindex:
           
           Takes a variable number of strings as the property
           name(s). These may contain wildcards as expanded by :mod:`fnmatch`.
           The name of the method does not matter.
           The method must take a property name as its sole argument.

        For both, `deps` is an iterable of property names, identifying which
        are the properties (both logical and concrete) which the
        logical property depends on.

        .. versionadded:: 1.99.1
           Introduced the decorator.

        .. versionchanged:: 1.99.2
           Added optional *deps* parameter.
        """

        @decorators.good_decorator
        def __decorator(_func):
            # creates the getters dictionary if needed 
            _dict = getattr(cls, support.metaclasses.LOGICAL_GETTERS_MAP_NAME, 
                            None)
            if _dict is None:
                _dict = dict()
                setattr(cls, support.metaclasses.LOGICAL_GETTERS_MAP_NAME, 
                        _dict)
                pass

            # names is an array which is set in the outer frame.
            # deps is a tuple/list which set int the outer frame
            if 0 == len(names): 
                if _func.__name__ in _dict:
                    # error: the name is used multiple times
                    raise ValueError("The same pattern is used multiple times")
                _dict[_func.__name__] = cls.__getinfo(_func, False, deps)
            else: 
                # annotates getters for all names
                for name in names: 
                    if name in _dict:
                        # error: the name is used multiple times
                        raise ValueError("The same pattern is "
                                         "used multiple times")
                    _dict[name] = cls.__getinfo(_func, True, deps)
                pass
            # here we can return whatever, it will in anycase
            # substituted by the metaclass constructor, to be a
            # property
            return _func

        if 1 == len(args) and isinstance(args[0], types.FunctionType):
            # decorator is used without arguments (args[0] contains
            # the decorated function)
            names = []  # names is used in __decorator @UnusedVariable
            deps = ()  # deps is used in __decorator @UnusedVariable
            return __decorator(args[0])
    
        # Here decorator is used with arguments
        # checks arguments types
        for arg in args: 
            if not isinstance(arg, types.StringType): 
                raise TypeError("Arguments of decorator must be strings")
            pass

        # here deps are checked
        _deps = kwargs.get(support.metaclasses.KWARG_NAME_DEPS, ())
        if not hasattr(_deps, '__iter__'):
                raise TypeError("Keyword argument '%s' must be an iterable" % 
                                support.metaclasses.KWARG_NAME_DEPS)
        for dep in _deps:
            if not isinstance(dep, types.StringType): 
                raise TypeError("Elements of keyword argument "
                                "'%s' must be strings" % \
                                support.metaclasses.KWARG_NAME_DEPS)
            pass
        # deps is the only supported keyword argument
        unsupported = set(kwargs) - set((support.metaclasses.KWARG_NAME_DEPS,))
        if unsupported:
            logger.warn("%s are unrecognized keyword arguments" % \
                        str(unsupported))
            pass

        names = args  # names is used in __decorator
        deps = _deps  # deps is used in __decorator

        return __decorator
    # ----------------------------------------------------------------------

    @classmethod
    @decorators.good_decorator_accepting_args
    def setter(cls, *args):
        """
        Decorate a method as a logical property setter. The counterpart to
        :meth:`getter`. Also comes in two flavours:

        .. method:: setter()
           :noindex:
           
           Uses the name of the method as the property name.
           The method must take one argument, the new value.

        .. method:: setter(one, two, ...)
           :noindex:
           
           Takes a variable number of strings as the property
           name(s). The name of the method does not matter.
           The method must take two arguments, the property name and new value.
        """
        
        @decorators.good_decorator
        def __decorator(_func):
            # creates the setters dictionary if needed 
            _dict = getattr(cls, support.metaclasses.LOGICAL_SETTERS_MAP_NAME, 
                            None)
            if _dict is None:
                _dict = dict()
                setattr(cls, support.metaclasses.LOGICAL_SETTERS_MAP_NAME, 
                        _dict)
                pass

            # names is an array which is set in the outer frame. 
            if 0 == len(names): 
                if _func.__name__ in _dict:
                    # error: the name is used multiple times
                    raise ValueError("The same pattern is used multiple times")
                _dict[_func.__name__] = cls.__setinfo(_func, False)
            else: 
                # annotates getters for all names
                for name in names: 
                    if name in _dict:
                        # error: the name is used multiple times
                        raise ValueError("The same pattern is used "
                                         "multiple times")
                    _dict[name] = cls.__setinfo(_func, True)
                    pass
                pass

            # here we can return whatever, it will in anycase
            # substituted by the metaclass constructor, to be a
            # property
            return _func

        if 1 == len(args) and isinstance(args[0], types.FunctionType):
            # decorator is used without arguments (args[0] contains
            # the decorated function)
            names = []  # names is used in __decorator @UnusedVariable
            return __decorator(args[0])
    
        # Here decorator is used with arguments
        # checks arguments types
        for arg in args: 
            if not isinstance(arg, types.StringType): 
                raise TypeError("Arguments of decorator must be strings")
            pass
        names = args  # names is used in __decorator
        return __decorator
    # ----------------------------------------------------------------------

    def __init__(self):
        Observer.__init__(self)
        
        self.__observers = []
        
        # keys are properties names, values are pairs (method,
        # kwargs|None) inside the observer. kwargs is the keyword
        # argument possibly specified when explicitly defining the
        # notification method in observers, and it is used to build
        # the NTInfo instance passed down when the notification method
        # is invoked. If kwargs is None (special case), the
        # notification method is "old style" (property_<name>_...) and
        # won't be receiving the property name.
        self.__value_notifications = {}
        self.__instance_notif_before = {}
        self.__instance_notif_after = {}
        self.__signal_notif = {}

        for key in self.get_properties(): self.register_property(key)

        # here OPs dependencies are reversed and pre-calculated
        self._calculate_logical_deps()

        # this stack is used to avoid spurious multiple notifications
        # which can happen otherwise when logical properties are
        # involved.
        self._notify_stack = [] 
        return

    def _has_observer(self):
        return bool(count_leaves((self.__value_notifications,
            self.__instance_notif_before, self.__instance_notif_after,
            self.__signal_notif)))

    def _calculate_logical_deps(self):
        """Internal service which calculates dependencies information
        based on those given with getters.
        
        The graph has to be reversed, as the getter tells that a
        property depends on a set of others, but the model needs to
        know how has to be notified (i.e. needs to know which OP is
        affected by an OP).  Only proximity of edges is considered,
        the rest is demanded at runtime)

        Result is stored inside internal dict __log_prop_deps which
        represents the dependencies graph.
        """        
        self.__log_prop_deps = {}  # the result goes here

        # this is used in messages
        _mod_cls = "%s.%s" % (self.__class__.__module__, 
                              self.__class__.__name__)

        logic_ops = ((name, opr.deps)
                     for name, opr in getmembers(type(self),\
  lambda x: isinstance(x, support.metaclasses.ObservablePropertyMeta.LogicalOP)
                                                ))
        # reverses the graph
        for name, deps in logic_ops:
            for dep in deps:
                if not self.has_property(dep):
                    raise ValueError("In class %s dependencies of logical "
                                     "property '%s' refer non-existant "
                                     "OP '%s'" % (_mod_cls, name, dep))
                rdeps = self.__log_prop_deps.get(dep, [])
                # name must appear only once in DAG
                assert name not in rdeps 
                rdeps.append(name)
                self.__log_prop_deps[dep] = rdeps
                pass
            pass
        # emits debugging info about dependencies
        for name, rdeps in self.__log_prop_deps.iteritems():
            logger.debug("In class %s changes to OP %s affects "
                         "logical OPs: %s",
                         _mod_cls, name, ", ".join(rdeps))
            pass

        # --------------------------------------------------
        # Here the graph is checked to be a DAG
        # --------------------------------------------------
        graph = dict((prop, frozenset(deps))
                     for prop, deps in self.__log_prop_deps.iteritems())

        # makes the graph total
        graph.update((prop, frozenset())
                     for prop in reduce(set.union, 
                                        map(set, graph.values()),
                                        set()) - set(graph.keys()))
        # DFS searching for leaves
        while True:
            leaves = frozenset(prop for prop, deps in graph.iteritems() 
                               if not deps)
            if not leaves: break
            # remove leaves from graph
            graph = dict((prop, (deps - leaves))
                         for prop, deps in graph.iteritems()
                         if prop not in leaves)
            pass

        # here remaining vertex are in a loop (over-approximated)
        if graph: 
            raise ValueError("In class %s found a loop among logical OPs: %s"\
                                 % (_mod_cls, ", ".join(graph.keys())))

        # here the graph is a DAG
        return

    def register_property(self, name):
        """Registers an existing property to be monitored, and sets up
        notifiers for notifications."""
        
        if name not in self.__value_notifications:
            self.__value_notifications[name] = []
            pass
        
        # registers observable wrappers
        prop = self.__get_prop_value(name)
        
        if isinstance(prop, ObsWrapperBase):
            prop.__add_model__(self, name)

            if isinstance(prop, Signal):
                if name not in self.__signal_notif:
                    self.__signal_notif[name] = []
                    pass
                pass
            else:
                if name not in self.__instance_notif_before:
                    self.__instance_notif_before[name] = []
                    pass
                if name not in self.__instance_notif_after:
                    self.__instance_notif_after[name] = []
                    pass
                pass
            pass

        return

    def has_property(self, name):
        """Returns true if given property name refers an observable
        property inside self or inside derived classes."""
        return name in self.get_properties()

    def register_observer(self, observer):
        """Register given observer among those observers which are
        interested in observing the model."""
        if observer in self.__observers: return  # not already registered

        assert isinstance(observer, Observer)
        self.__observers.append(observer)
        for key in self.get_properties():
            self.__add_observer_notification(observer, key)
            pass
        
        return
            
    def unregister_observer(self, observer):
        """Unregister the given observer that is no longer interested
        in observing the model."""
        assert isinstance(observer, Observer)

        if observer not in self.__observers: return
        for key in self.get_properties():
            self.__remove_observer_notification(observer, key)
            pass
        
        self.__observers.remove(observer) 
        return

    def _reset_property_notification(self, prop_name, old=None):
        """Called when it has be done an assignment that changes the
        type of a property or the instance of the property has been
        changed to a different instance. In this case it must be
        unregistered and registered again. Optional parameter old has
        to be used when the old value is an instance (derived from 
        ObsWrapperBase) which needs to unregisters from the model, via
        a call to method old.__remove_model__(model, prop_name)"""

        # unregister_property
        if isinstance(old, ObsWrapperBase): 
            old.__remove_model__(self, prop_name)
            pass

        self.register_property(prop_name)

        for observer in self.__observers:
            self.__remove_observer_notification(observer, prop_name)
            self.__add_observer_notification(observer, prop_name)
            pass
        return
    
    def get_properties(self):
        """
        All observable properties accessible from this instance.

        :rtype: frozenset of strings
        """
        return getattr(self, support.metaclasses.ALL_OBS_SET, frozenset())

    def __add_observer_notification(self, observer, prop_name):
        """
        Find observing methods and store them for later notification.

        *observer* an instance.
        
        *prop_name* a string.

        This checks for magic names as well as methods explicitly added through
        decorators or at runtime. In the latter case the type of the
        notification is inferred from the number of arguments it takes.
        """
        value = self.__get_prop_value(prop_name)

        # --- Some services ---
        def getmeth(_format, numargs):
            name = _format % prop_name
            meth = getattr(observer, name)
            args, varargs, _, _ = inspect.getargspec(meth)
            if not varargs and len(args) != numargs:
                logger.warn("Ignoring notification %s: exactly %d arguments"
                    " are expected", name, numargs)
                raise AttributeError
            return meth

        def add_value(notification, kw=None):
            pair = (notification, kw)
            if pair in self.__value_notifications[prop_name]: return
            logger.debug("Will call %s.%s after assignment to %s.%s",
                observer.__class__.__name__, notification.__name__,
                self.__class__.__name__, prop_name)
            self.__value_notifications[prop_name].append(pair)
            return

        def add_before(notification, kw=None):
            if (not isinstance(value, ObsWrapperBase) or 
                isinstance(value, Signal)): 
                return

            pair = (notification, kw)
            if pair in self.__instance_notif_before[prop_name]: return
            logger.debug("Will call %s.%s before mutation of %s.%s",
                observer.__class__.__name__, notification.__name__,
                self.__class__.__name__, prop_name)
            self.__instance_notif_before[prop_name].append(pair)
            return

        def add_after(notification, kw=None):
            if (not isinstance(value, ObsWrapperBase) or 
                isinstance(value, Signal)):
                return
            pair = (notification, kw)
            if pair in self.__instance_notif_after[prop_name]: return
            logger.debug("Will call %s.%s after mutation of %s.%s",
                observer.__class__.__name__, notification.__name__,
                self.__class__.__name__, prop_name)
            self.__instance_notif_after[prop_name].append(pair)
            return

        def add_signal(notification, kw=None):
            if not isinstance(value, Signal): return
            pair = (notification, kw)
            if pair in self.__signal_notif[prop_name]: return
            logger.debug("Will call %s.%s after emit on %s.%s",
                observer.__class__.__name__, notification.__name__,
                self.__class__.__name__, prop_name)
            self.__signal_notif[prop_name].append(pair)
            return
        # ---------------------

        try: notification = getmeth("property_%s_signal_emit", 3)
        except AttributeError: pass
        else: add_signal(notification)

        try: notification = getmeth("property_%s_value_change", 4)
        except AttributeError: pass
        else: add_value(notification)

        try: notification = getmeth("property_%s_before_change", 6)
        except AttributeError: pass
        else: add_before(notification)

        try: notification = getmeth("property_%s_after_change", 7)
        except AttributeError: pass
        else: add_after(notification)
        
        # here explicit notification methods are handled (those which
        # have been statically or dynamically registered)
        type_to_adding_method = {
            'assign' : add_value,
            'before' : add_before, 
            'after'  : add_after, 
            'signal' : add_signal,
            }
        
        for meth in observer.get_observing_methods(prop_name):
            added = False
            kw = observer.get_observing_method_kwargs(prop_name, meth)
            for flag, adding_meth in type_to_adding_method.iteritems():
                if flag in kw: 
                    added = True
                    adding_meth(meth, kw)
                    pass
                pass
            if not added: raise ValueError("In %s notification method %s is "
                                           "marked to be observing property "
                                           "'%s', but no notification type "
                                           "information were specified." %
                                           (observer.__class__, 
                                            meth.__name__, prop_name))
            pass
        
        return

    def __remove_observer_notification(self, observer, prop_name):
        """
        Remove all stored notifications.
        
        *observer* an instance.
        
        *prop_name* a string.
        """

        def side_effect(seq):
            for meth, kw in reversed(seq):
                if meth.im_self is observer:
                    seq.remove((meth, kw))
                    yield meth

        for meth in side_effect(self.__value_notifications.get(prop_name, ())):
            logger.debug("Stop calling %s.%s after assignment to %s.%s",
                observer.__class__.__name__, meth.__name__,
                self.__class__.__name__, prop_name)
        
        for meth in side_effect(self.__signal_notif.get(prop_name, ())):
            logger.debug("Stop calling %s.%s after emit on %s.%s",
                observer.__class__.__name__, meth.__name__,
                self.__class__.__name__, prop_name)
        
        for meth in side_effect(
                        self.__instance_notif_before.get(prop_name, ())):
            logger.debug("Stop calling %s.%s before mutation of %s.%s",
                observer.__class__.__name__, meth.__name__,
                self.__class__.__name__, prop_name)
        
        for meth in side_effect(
                        self.__instance_notif_after.get(prop_name, ())):
            logger.debug("Stop calling %s.%s after mutation of %s.%s",
                observer.__class__.__name__, meth.__name__,
                self.__class__.__name__, prop_name)
        
        return

    def __notify_observer__(self, observer, method, *args, **kwargs):
        """This can be overridden by derived class in order to call
        the method in a different manner (for example, in
        multithreading, or a rpc, etc.)  This implementation simply
        calls the given method with the given arguments"""
        return method(*args, **kwargs)

    def __before_property_value_change__(self, prop_name):
        """This is called right before the value of a property gets
        changed, and before a property change notification is
        sent. This is called before calling
        notify_property_value_change in order to first collect all the
        old values of the properties whose value is declared to be
        dependend on this property. Returns a tuple containing the old
        values (the values before the assignments to prop_name), among
        with other information. The returned tuple has to be passed to
        __after_property_value_change__. All this procedure is done by
        the setter's code which is generated by the metaclass."""

        return tuple((self, name, getattr(self, name))
                     for name in self._get_logical_deps(prop_name)
                     if name not in self._notify_stack)

    def _get_logical_deps(self, prop_name):
        """Returns an iterator over a sequence of property names,
        which has to e notified upon any value modification of
        prop_name. used internally by __before_property_value_change__"""

        if prop_name not in self.__log_prop_deps: return  # stop iteration

        alread_visited = set()
        to_be_visited = self.__log_prop_deps[prop_name][:]  # copy
        while to_be_visited:
            x = to_be_visited.pop(0)
            if x not in alread_visited:
                yield x
                alread_visited.add(x)
                children = self.__log_prop_deps.get(x, [])
                to_be_visited += children
                pass
            pass
        return            

    def __after_property_value_change__(self, prop_name, old_vals):
        """This is called after the value of a property is
        changed. This is called while calling
        notify_property_value_change in order to notify all the
        observers which are interested in observing properties whose
        value is declared to be dependend on this property. The
        old_vals tuple is the value returned by the previous call to
        __before_property_value_change__. All this procedure is done
        by the setter's code which is generated by the metaclass."""
        for model, name, val in old_vals:
            model.notify_property_value_change(name, val, getattr(model, name))
            pass
        return

    # -------------------------------------------------------------
    #            Notifiers:
    # -------------------------------------------------------------
    
    def notify_property_value_change(self, prop_name, old, new):
        """
        Send a notification to all registered observers.

        *old* the value before the change occured.
        """

        assert prop_name in self.__value_notifications
        for method, kw in self.__value_notifications[prop_name][:]:
            obs = method.im_self
            # spuriousness (ticket:38) is checked here
            if kw and "spurious" in kw: spurious = kw['spurious']
            else: spurious = obs.accepts_spurious_change()
            
            # notification occurs checking spuriousness of the observer
            if old != new or spurious:
                if kw is None:  # old style call without name
                    self.__notify_observer__(obs, method,
                                             self, old, new)
                elif 'old_style_call' in kw:  # old style call with name
                    self.__notify_observer__(obs, method,
                                             self, prop_name, old, new)
                else: 
                    # New style explicit notification.
                    # notice that named arguments overwrite any
                    # existing key:val in kw, which is precisely what
                    # it is expected to happen
                    info = NTInfo('assign',
                                  kw, model=self, prop_name=prop_name, 
                                  old=old, new=new)
                    self.__notify_observer__(obs, method, 
                                             self, prop_name, info)
                    pass
                pass
            pass
        return                

    def notify_method_before_change(self, prop_name, instance, meth_name,
                                    args, kwargs):
        """
        Send a notification to all registered observers.

        *instance* the object stored in the property.

        *meth_name* name of the method we are about to call on *instance*.
        """
        assert prop_name in self.__instance_notif_before
        for method, kw in self.__instance_notif_before[prop_name][:]:
            obs = method.im_self
            # notifies the change
            if kw is None:  # old style call without name
                self.__notify_observer__(obs, method,
                                         self, instance,
                                         meth_name, args, kwargs)
            elif 'old_style_call' in kw:  # old style call with name
                self.__notify_observer__(obs, method,
                                         self, prop_name, instance,
                                         meth_name, args, kwargs)                
            else: 
                # New style explicit notification.
                # notice that named arguments overwrite any
                # existing key:val in kw, which is precisely what
                # it is expected to happen
                info = NTInfo('before',
                              kw, 
                              model=self, prop_name=prop_name, 
                              instance=instance, method_name=meth_name, 
                              args=args, kwargs=kwargs)
                self.__notify_observer__(obs, method, 
                                         self, prop_name, info)
                pass
            pass
        return                

    def notify_method_after_change(self, prop_name, instance, meth_name,
                                   res, args, kwargs):
        """
        Send a notification to all registered observers.

        *args* the arguments we just passed to *meth_name*.

        *res* the return value of the method call.
        """
        assert prop_name in self.__instance_notif_after
        for method, kw in self.__instance_notif_after[prop_name][:]:
            obs = method.im_self
            # notifies the change
            if kw is None:  # old style call without name
                self.__notify_observer__(obs, method,
                                         self, instance,
                                         meth_name, res, args, kwargs) 
            elif 'old_style_call' in kw:  # old style call with name
                self.__notify_observer__(obs, method,
                                         self, prop_name, instance,
                                         meth_name, res, args, kwargs) 
            else: 
                # New style explicit notification.
                # notice that named arguments overwrite any
                # existing key:val in kw, which is precisely what
                # it is expected to happen
                info = NTInfo('after',
                              kw, 
                              model=self, prop_name=prop_name, 
                              instance=instance, method_name=meth_name, 
                              result=res, args=args, kwargs=kwargs)
                self.__notify_observer__(obs, method, 
                                         self, prop_name, info)
                pass            
            pass
        return

    def notify_signal_emit(self, prop_name, arg):
        """
        Emit a signal to all registered observers.

        *prop_name* the property storing the :class:`~gtkmvc.observable.Signal`
        instance.

        *arg* one arbitrary argument passed to observing methods.
        """
        assert prop_name in self.__signal_notif        
        for method, kw in self.__signal_notif[prop_name][:]:
            obs = method.im_self
            # notifies the signal emit
            if kw is None:  # old style call, without name
                self.__notify_observer__(obs, method,
                                         self, arg)
            elif 'old_style_call' in kw:  # old style call with name
                self.__notify_observer__(obs, method,
                                         self, prop_name, arg)
            else:
                # New style explicit notification.
                # notice that named arguments overwrite any
                # existing key:val in kw, which is precisely what
                # it is expected to happen
                info = NTInfo('signal',
                              kw, 
                              model=self, prop_name=prop_name, arg=arg)
                self.__notify_observer__(obs, method, 
                                         self, prop_name, info)
                pass
            pass
        return
        
    def __get_prop_value(self, name):
        """Returns the property value, given its name."""
        return getattr(self, "_prop_%s" % name, None)

    pass  # end of class Model
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
class TreeStoreModel (Model, gtk.TreeStore):
    """Use this class as base class for your model derived by
    gtk.TreeStore"""
    __metaclass__ = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, column_type, *args):
        gtk.TreeStore.__init__(self, column_type, *args)
        Model.__init__(self)
        return
    pass  # end of class


# ----------------------------------------------------------------------
class ListStoreModel (Model, gtk.ListStore):
    """Use this class as base class for your model derived by
    gtk.ListStore"""
    __metaclass__ = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, column_type, *args):
        gtk.ListStore.__init__(self, column_type, *args)
        Model.__init__(self)
        return
    pass  # end of class
    

# ----------------------------------------------------------------------
class TextBufferModel (Model, gtk.TextBuffer):
    """Use this class as base class for your model derived by
    gtk.TextBuffer"""
    __metaclass__ = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, table=None):
        gtk.TextBuffer.__init__(self, table)
        Model.__init__(self)
        return
    pass  # end of class


# ----------------------------------------------------------------------
try: 
    from sqlobject.inheritance import InheritableSQLObject  # @UnresolvedImport
except: 
    pass  # sqlobject not available
else:
    class SQLObjectModel(InheritableSQLObject, Model):
        """
        SQLObject uses a class's name for the corresponding table, so
        subclasses of this need application-wide unique names, no
        matter what package they're in!

        After defining subclasses (not before!) you have to call
        ``.createTable`` on each, including SQLObjectModel itself.
        """

        __metaclass__ = support.metaclasses.ObservablePropertyMetaSQL

        def _init(self, *args, **kargs):
            # Using __init__ or not calling super _init results in incomplete
            # objects. Model init will then raise missing _SO_writeLock.
            InheritableSQLObject._init(self, *args, **kargs)
            Model.__init__(self)
            return

        @classmethod
        def createTables(cls, *args, **kargs):
            """
            Recursively calls InheritableSQLObject.createTable on this
            and all subclasses, passing any arguments on.

            Call this during startup, after setting up the DB
            connection and importing all your persistent models. Pass
            ``ifNotExists=True unless`` you want to wipe the database.
            """
            cls.createTable(*args, **kargs)
            for child in cls.__subclasses__():
                child.createTables(*args, **kargs)
                pass
            return
        
        pass  # end of class
    pass 
# ----------------------------------------------------------------------
