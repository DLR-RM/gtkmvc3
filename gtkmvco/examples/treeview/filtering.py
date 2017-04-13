# PYGTKMVC TreeView contribution handler
# Copyright (C) 2011  Tobias Weber
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.

class get_visible_function(object):
    def __init__(self, model, column=0):
        """
        *model* is a :class:`gtk.TreeModelFilter` instance.

        *column* is an integer adressing the column that holds items.
        """
        self.model = model
        self.column = column
        self.checks = ()
        model.set_visible_func(self)

    def __call__(self, tree, iter):
        obj = tree.get_value(iter, self.column)
        for function, attribute in self.checks:
            if not function(getattr(obj, attribute)):
                return False
        return True

    def refilter(self, predicates, module):
        """
        *predicates* a sequence of 3-tuples.

        *module* an object created with `import`.

        Predicates have the following format:
    
        *attribute* a string naming an attribute of items.

        *function* a string naming a factory callable in *module*.

        *argument* can be anything. This will be passed to *function* as its
        sole argument. The result must be a callable that takes a value of
        *attribute* and returns a boolean.
        We do this to make the refilter after changing criteria faster.

        The function we return will lazily evaluate the predicates and logically
        combine their results in an AND fashion.
        """
        self.checks = tuple(
            (getattr(module, factory)(argument), attribute)
            for attribute, factory, argument in predicates
            )
        self.model.refilter()
