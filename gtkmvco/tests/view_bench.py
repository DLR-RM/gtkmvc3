"""
Shows that memoization makes sense.
"""

import timeit

import _importer
import gtkmvc

glade = gtkmvc.View(glade='adapter7.glade')
build = gtkmvc.View(builder='adapter19.ui')

# Cause auto widget extraction.
names = tuple(glade)

# Dictionary.
t = timeit.Timer("""
    for name in names:
        glade.autoWidgets[name]
    """, "from __main__ import glade, names")
print t.timeit() #1.6

# Doesn't save much.
xml = glade.glade_xmlWidgets[0]
t = timeit.Timer("""
    for name in names:
        xml.get_widget(name)
    """, "from __main__ import xml, names")
print t.timeit() #5.8

t = timeit.Timer("""
    for name in names:
        build._builder.get_object(name)
    """, "from __main__ import build, names")
print t.timeit() #19
