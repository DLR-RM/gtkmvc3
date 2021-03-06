#  -------------------------------------------------------------------------
#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.
#  -------------------------------------------------------------------------

import inspect
import fnmatch
import functools

from gtkmvc3.support import decorators, log


class NTInfo (dict):
    # At least one of the keys in this set is required when constructing
    __ONE_REQUESTED = frozenset("assign before after signal".split())
    __ALL_REQUESTED = frozenset("model prop_name".split())

    def __init__(self, _type, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

        # checks the content provided by the user
        if not (_type in self and self[_type]):
            raise KeyError("flag '%s' must be set in given arguments" % _type)

        # all requested are provided by the framework, not the user
        assert NTInfo.__ALL_REQUESTED <= set(self)

        # now removes all type-flags not related to _type
        for flag in NTInfo.__ONE_REQUESTED:
            if flag != _type and flag in self:
                del self[flag]

    def __getattr__(self, name):
        """
        All dictionary keys are also available as attributes.
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError("NTInfo object has no attribute '%s'.\n"
                                 "Existing attributes are: %s" % \
                                 (name, str(self)))


# ----------------------------------------------------------------------
@decorators.good_decorator_accepting_args
def observes(*args):
    """
    Decorate a method in an :class:`Observer` subclass as a notification.
    Takes one to many property names as strings. If any of them changes
    in a model we observe, the method is called. The name of the property
    will be passed to the method.

    The type of notification is inferred from the number of arguments. Valid
    signature are::

      def value_notify(self, model, name, old, new)
      def before_notify(self, model, name, instance, method_name, args,
                        kwargs)
      def after_notify(self, model, name, instance, method_name, res, args,
                       kwargs)
      def signal_notify(self, model, name, arg)

    .. versionadded:: 1.99.0

    .. deprecated:: 1.99.1
       Use :meth:`Observer.observe` instead, which offers more features.
    """

    @decorators.good_decorator
    def _decorator(_notified):
        # marks the method with observed properties
        _list = getattr(_notified, Observer._CUST_OBS_, list())

        # here the notificaion type is inferred out of the number of
        # arguments of the notification method. This is not
        # particularly robust.
        margs, mvarargs, _, _ = inspect.getargspec(_notified)
        mnumargs = len(margs)
        if not mvarargs:
            args_to_type = {4: 'signal',
                            5: 'assign',
                            7: 'before',
                            8: 'after',
                            }
            try :
                type_kw = args_to_type[mnumargs]
                # warning: flag _old_style_call is used this as
                # deprecated call mechanism like in
                # <property_<name>_...
                _list += [(arg, dict({type_kw : True,
                                      'old_style_call' : True}))
                          for arg in args]
                setattr(_notified, Observer._CUST_OBS_, _list)

            except KeyError:
                log.logger.warn("Ignoring notification %s: wrong number of"
                                " arguments (given %d, expected in (%s))",
                                _notified.__name__, mnumargs,
                                ",".join(map(str, args_to_type)))
        else:
            log.logger.warn("Ignoring notification %s: variable arguments"
                            " prevent type inference", _notified.__name__)
        return _notified

    # checks arguments
    if 0 == len(args):
        raise TypeError("decorator observe() takes one of more "
                        "arguments (0 given)")
    if any(a for a in args if not isinstance(a, str)):
        raise TypeError("decorator observe() takes only strings as arguments")

    log.logger.warning("Decorator observer.observers is deprecated:"
                       "use Observer.observe instead")
    return _decorator
# ----------------------------------------------------------------------


# this used for pattern matching
WILDCARDS = frozenset("[]!*?")


class Observer (object):
    """
    .. note::

       Most methods in this class are used internally by the
       framework.  Do not override them in subclasses.
    """

    # this is internal
    _CUST_OBS_ = "__custom_observes__"
    # ----------------------------------------------------------------------

    @classmethod
    @decorators.good_decorator_accepting_args
    def observe(cls, *args, **kwargs):
        """
        Mark a method as receiving notifications. Comes in two flavours:

        .. method:: observe(name, **types)
           :noindex:

           A decorator living in the class. Can be applied more than once to
           the same method, provided the names differ.

           *name* is the property we want to be notified about as a
           string.

           .. Note::

              Alternatively, *name* can be a pattern for matching
              property names, meaning it can contain wildcards
              character like in module `fnmatch
              <http://docs.python.org/library/fnmatch.html>`_ in
              Python library. However, if wildcards are used in name,
              only *one* `observe` can be used for a given
              notification method, or else `ValueError` exception is
              raised when the Observer class is instantiated.

              .. versionadded:: 1.99.2

           *types* are boolean values denoting the types of
           notifications desired. At least one of the following has to be
           passed as True: assign, before, after, signal.

           Excess keyword arguments are passed to the method as part of the
           info dictionary.

        .. method:: observe(callable, name, **types)
           :noindex:

           An instance method to define notifications at runtime. Works as
           above.

           *callable* is the method to send notifications to. The effect will
           be as if this had been decorated.

        In all cases the notification method must take exactly three
        arguments: the model object, the name of the property that changed,
        and an :class:`NTInfo` object describing the change.

        .. warning::

           Due to limitation in the dynamic registration (in version
           1.99.1), declarations of dynamic notifications must occur
           before registering self as an observer of the models whose
           properties the notifications are supposed to be
           observing. A hack for this limitation, is to first relieve
           any interesting model before dynamically register the
           notifications, and then re-observe those models.

        .. versionadded:: 1.99.1
        """

        @decorators.good_decorator
        def _decorator(_notified):
            # marks the method with observed properties
            _list = getattr(_notified, Observer._CUST_OBS_, list())
            _list.append((name, kwargs))
            setattr(_notified, Observer._CUST_OBS_, _list)
            return _notified

        # handles arguments
        if args and isinstance(args[0], cls):
            # Used as instance method, for declaring notifications
            # dynamically
            if len(args) != 3:
                raise TypeError("observe() takes exactly three arguments"
                                " when called (%d given)" % len(args))

            self = args[0]
            notified = args[1]
            name = args[2]

            assert isinstance(self, Observer), "Method Observer.observe " \
                "must be called with an Observer instance as first argument"
            if not callable(notified):
                raise TypeError("Second argument of observe() "
                                "must be a callable")
            if not isinstance(name, str):
                raise TypeError("Third argument of observe() must be a string")

            self.__register_notification(name, notified, kwargs)
            return None

        # used statically as decorator
        if len(args) != 1:
            raise TypeError("observe() takes exactly one argument when used"
                            " as decorator (%d given)" % len(args))
        name = args[0]
        if not isinstance(name, str):
            raise TypeError("First argument of observe() must be a string")
        return _decorator
    # ----------------------------------------------------------------------

    def __init__(self, model=None, spurious=False):
        """
        *model* is passed to :meth:`observe_model` if given.

        *spurious* indicates interest to be notified even when
        the value hasn't changed, like for: ::

         model.prop = model.prop

        .. versionadded:: 1.2.0
           Before that observers had to filter out spurious
           notifications themselves, as if the default was `True`. With
           :class:`~gtkmvc3.observable.Signal` support this is no longer
           necessary.
        """

        # --------------------------------------------------------- #
        # This turns the decorator 'observe' an instance method
        def __observe(*args, **kwargs):
            self.__original_observe(self, *args, **kwargs)

        __observe.__name__ = self.observe.__name__
        __observe.__doc__ = self.observe.__doc__
        self.__original_observe = self.observe
        self.observe = __observe
        # --------------------------------------------------------- #

        self.__accepts_spurious__ = spurious

        # NOTE: In rev. 202 these maps were unified into
        #   __PROP_TO_METHS only (the map contained pairs (method,
        #   args). However, this broke backward compatibility of code
        #   accessing the map through
        #   get_observing_methods. Now the informatio is split
        #   and the original information restored. To access the
        #   additional information (number of additional arguments
        #   required by observing methods) use the newly added methods.

        # Private maps: do not change/access them directly, use
        # methods to access them:
        self.__PROP_TO_METHS = {}  # prop name --> set of observing methods
        self.__METH_TO_PROPS = {}  # method --> set of observed properties

        # like __PROP_TO_METHS but only for pattern names (to optimize search)
        self.__PAT_TO_METHS = {}

        self.__METH_TO_PAT = {}  # method --> pattern
        self.__PAT_METH_TO_KWARGS = {}  # (pattern, method) --> info

        processed_props = set()  # tracks already processed properties

        # searches all custom observer methods
        for cls in inspect.getmro(type(self)):
            # list of (method-name, method-object, list of (prop-name, kwargs))
            meths = [(name, meth, getattr(meth, Observer._CUST_OBS_))
                     for name, meth in cls.__dict__.items()
                     if (inspect.isfunction(meth) and
                         hasattr(meth, Observer._CUST_OBS_))]

            # props processed in this class. This is used to avoid
            # processing the same props in base classes.
            cls_processed_props = set()

            # since this is traversed top-bottom in the mro, the
            # first found match is the one to care
            for name, meth, pnames_ka in meths:
                _method = getattr(self, name)  # the most top avail method

                # WARNING! Here we store the top-level method in the
                # mro, not the (unbound) method which has been
                # declared by the user with the decorator.
                for pname, ka in pnames_ka:
                    if pname not in processed_props:
                        self.__register_notification(pname, _method, ka)
                        cls_processed_props.add(pname)

            # accumulates props processed in this class
            processed_props |= cls_processed_props

        if model:
            self.observe_model(model)

    def observe_model(self, model):
        """Starts observing the given model"""
        return model.register_observer(self)

    def relieve_model(self, model):
        """Stops observing the given model"""
        return model.unregister_observer(self)

    def accepts_spurious_change(self):
        """
        Returns True if this observer is interested in receiving
        spurious value changes. This is queried by the model when
        notifying a value change."""
        return self.__accepts_spurious__

    def get_observing_methods(self, prop_name):
        """
        Return a possibly empty set of callables registered with
        :meth:`observe` for *prop_name*. The returned set includes
        those notifications which have been registered by means of
        patterns matching prop_name.

        .. versionadded:: 1.99.1
           Replaces :meth:`get_custom_observing_methods`.
        """
        # searches in pattern and in map
        return (functools.reduce(set.union,
                                 (meths
                                  for pat, meths in self.__PAT_TO_METHS.items()
                                  if fnmatch.fnmatch(prop_name, pat)),
                                 set()) |
                self.__PROP_TO_METHS.get(prop_name, set()))

    # this is done to keep backward compatibility
    get_custom_observing_methods = get_observing_methods

    def get_observing_method_kwargs(self, prop_name, method):
        """
        Returns the keyword arguments which were specified when
        declaring a notification method, either statically or
        dynamically with :meth:`Observer.observe`.

        Since patterns may be involved when declaring the
        notifications, first exact match is checked, and then the
        single-allowed pattern is checked, if there is any.

        *method* a callable that was registered with
        :meth:`observe`.

        :rtype: dict
        """
        # exact match have precedence
        if (prop_name, method) in self.__PAT_METH_TO_KWARGS:
            return self.__PAT_METH_TO_KWARGS[(prop_name, method)]

        # checks pattern
        if method in self.__METH_TO_PAT:
            prop_name = self.__METH_TO_PAT[method]

        return self.__PAT_METH_TO_KWARGS[(prop_name, method)]

    def remove_observing_method(self, prop_names, method):
        """
        Remove dynamic notifications.

        *method* a callable that was registered with :meth:`observe`.

        *prop_names* a sequence of strings. This need not correspond to any
        one `observe` call.

        .. note::

           This can revert even the effects of decorator `observe` at
           runtime. Don't.
        """
        for prop_name in prop_names:
            if prop_name in self.__PROP_TO_METHS:
                # exact match
                self.__PROP_TO_METHS[prop_name].remove(method)
                del self.__PAT_METH_TO_KWARGS[(prop_name, method)]
            elif method in self.__METH_TO_PAT:
                # found a pattern matching
                pat = self.__METH_TO_PAT[method]
                if fnmatch.fnmatch(prop_name, pat):
                    del self.__METH_TO_PAT[method]
                    self.__PAT_TO_METHS[pat].remove(method)

                del self.__PAT_METH_TO_KWARGS[(pat, method)]

    def is_observing_method(self, prop_name, method):
        """
        Returns `True` if the given method was previously added as an
        observing method, either dynamically or via decorator.
        """
        if (prop_name, method) in self.__PAT_METH_TO_KWARGS:
            return True
        if method in self.__METH_TO_PAT:
            pat = self.__METH_TO_PAT[method]
            if fnmatch.fnmatch(prop_name, pat):
                return True

        return False

    def __register_notification(self, prop_name, method, kwargs):
        """Internal service which associates the given property name
        to the method, and the (prop_name, method) with the given
        kwargs dictionary. If needed merges the dictionary, if the
        given (prop_name, method) pair was already registered (in this
        case the last registration wins in case of overlapping.)

        If given prop_name and method have been already registered, a
        ValueError exception is raised."""

        key = (prop_name, method)
        if key in self.__PAT_METH_TO_KWARGS:
            raise ValueError("In class %s method '%s' has been declared "
                             "to be a notification for pattern '%s' "
                             "multiple times (only one is allowed)." % \
                                 (self.__class__,
                                  method.__name__, prop_name))
        if frozenset(prop_name) & WILDCARDS:
            # checks that at most one pattern is specified per-method:
            # (see ticket:31#comment:7 and following)
            if (method in self.__METH_TO_PAT or
                (method in self.__METH_TO_PROPS and
                 self.__METH_TO_PROPS[method])):
                raise ValueError("In class %s multiple patterns have been "
                                 "used to declare method '%s' to be a "
                                 "notification (only one is allowed.)" % \
                                 (self.__class__, method.__name__))

            # for the sake of efficiency, method to patterns map is kept
            self.__METH_TO_PAT[method] = prop_name

            # the name contains wildcards
            _dict = self.__PAT_TO_METHS

        else:
            # check that it was not used for patterns
            if method in self.__METH_TO_PAT:
                raise ValueError("In class %s multiple patterns have been "
                                 "used to declare method '%s' to be a "
                                 "notification (only one is allowed.)" % \
                                 (self.__class__, method.__name__))

            _dict = self.__PROP_TO_METHS
            if method not in self.__METH_TO_PROPS:
                self.__METH_TO_PROPS[method] = set()

            self.__METH_TO_PROPS[method].add(prop_name)

        # fills the internal structures
        if prop_name not in _dict:
            _dict[prop_name] = set()

        _dict[prop_name].add(method)

        self.__PAT_METH_TO_KWARGS[key] = kwargs
# ----------------------------------------------------------------------
