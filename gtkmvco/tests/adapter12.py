import unittest

import gtk

from _importer import refresh_gui

import gtkmvc
# Importing this as default.__def_adapter or __def_adapter would get mangled
# with the name of the test class, because double underscores get replaced
# very early.
from gtkmvc.adapters.default import __def_adapter as DEF

BAR = (gtk.Toolbar, "style-changed", gtk.Toolbar.get_style,
    gtk.Toolbar.set_style, gtk.ToolbarStyle, None)

class Model(gtkmvc.Model):
    bar = gtk.TOOLBAR_TEXT
    __observables__ = ["bar"]

class Defaults(unittest.TestCase):
    def setUp(self):
        # Copy.
        self.backup = tuple(DEF)

        self.m = Model()
        self.v = gtkmvc.View()
        self.v["bar"] = gtk.Toolbar()
        # Relying on auto_adapt=False as the default.
        self.c = gtkmvc.Controller(self.m, self.v)
        refresh_gui()

    def tearDown(self):
        # Replace in place.
        DEF[0:len(DEF)] = self.backup
        # TODO remove memoization from framework because the speed increase is
        # minimal and it likely messes up remove_adapter.
        gtkmvc.adapters.default.__memoize__ = {} 

    def adapterTest(self):
        """
        Not called by the unittest.main()
        """
        self.c.adapt()
        self.assertEqual(gtk.TOOLBAR_TEXT, self.v["bar"].get_style())
        self.v["bar"].set_style(gtk.TOOLBAR_ICONS)
        self.assertEqual(gtk.TOOLBAR_ICONS, self.m.bar)

    def testNegative(self):
        # Adapting toolbars doesn't make sense, so there shouldn't be a
        # default in the framework.
        self.assertRaises(TypeError, lambda: self.c.adapt())

    def testManual(self):
        DEF.append(BAR)
        self.adapterTest()

    def testCall(self):
        # TODO test insertion/overriding an existing default.
        gtkmvc.adapters.default.add_adapter(*BAR)
        self.adapterTest()

    def testAPI(self):
        self.assertFalse(gtkmvc.adapters.default.remove_adapter(gtk.Toolbar))
        gtkmvc.adapters.default.add_adapter(*BAR)
        self.assertTrue(gtkmvc.adapters.default.remove_adapter(gtk.Toolbar))
        self.assertRaises(TypeError, lambda: self.c.adapt())

if __name__ == "__main__":
    unittest.main()
