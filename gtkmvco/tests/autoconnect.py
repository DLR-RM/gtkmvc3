import unittest

import gtk

from _importer import refresh_gui
import gtkmvc

class Super(gtkmvc.Controller):
    def __init__(self, **kwargs):
        self.calls = []

        v = gtkmvc.View()
        v['main_window'] = w = gtk.Window()
        v['button'] = b = gtk.Button()
        w.add(b)

        gtkmvc.Controller.__init__(self, gtkmvc.Model(), v, **kwargs)
        refresh_gui()

    def on_button__clicked(self, widget):
        self.calls.append(widget)

class Controller(Super):
    handlers = "class"

    def on_main_window__delete_event(self, widget, event):
        self.calls.append(widget)

class AutoConnect(unittest.TestCase):
    def testDefault(self):
        c = Super()
        w = c.view['button']
        w.clicked()
        self.assertEqual([], c.calls)

    def testArgument(self):
        c = Super(handlers="class")
        w = c.view['button']
        w.clicked()
        self.assertEqual([w], c.calls)

    def testAttribute(self):
        c = Controller()
        w = c.view['button']
        w.clicked()
        self.assertEqual([w], c.calls)

    def testUnderscores(self):
        c = Controller()
        w = c.view['main_window']
        # Didn't find a better way.
        w.emit('delete-event', gtk.gdk.Event(gtk.gdk.DELETE))
        self.assertEqual([w], c.calls)

if __name__ == "__main__":
    unittest.main()
