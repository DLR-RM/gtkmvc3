import unittest

import gtk

from _importer import refresh_gui

import gtkmvc
from gtkmvc.adapters.basic import Adapter

class Model(gtkmvc.Model):
    en1 = 10.0
    __observables__ = ["en1"]

class Controller(gtkmvc.Controller):
    def on_button1_clicked(self, button):
        self.model.en1 += 1

class TwoForOne(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(glade="adapters.glade", top="window1")
        self.c = Controller(self.m, self.v)
        refresh_gui()

    def testArguments(self):
        errors = []
        def handle(adapter, name, value):
            errors.append((adapter, name, value))
            adapter.update_widget()

        e = Adapter(self.m, "en1",
            prop_read=lambda v: v/2.0,
            prop_write=lambda v: float(v)*2,
            value_error=handle,
            prop_cast=False,
            )
        e.connect_widget(self.v["entry1"])

        l = Adapter(self.m, "en1")
        l.connect_widget(self.v["label1"],
            setter=lambda w, v: w.set_markup("<big><b>%.2f</b></big>" % v))

        self.assertEqual("5.0", self.v["entry1"].get_text())
        self.assertEqual("10.00", self.v["label1"].get_text())

        # This fails on RHEL because the old gtk.Entry cannot go directly from
        # one string to another. It will first empty itself and emit a signal
        # for that. At this point prop_write raises and the entry is reset. It
        # then "types" the 1 so we end up with 15.
        # https://bugzilla.gnome.org/show_bug.cgi?id=64998
        if gtk.gtk_version == (2, 10, 4):
            return
        self.v["entry1"].set_text("1")
        self.assertEqual("2.00", self.v["label1"].get_text())

        self.v["button1"].clicked()
        self.assertEqual("1.5", self.v["entry1"].get_text())
        self.assertEqual("3.00", self.v["label1"].get_text())

        self.v["entry1"].set_text("?")
        self.assertEqual((e, "en1", "?"), errors[-1])
        self.assertEqual("1.5", self.v["entry1"].get_text())
        self.assertEqual("3.00", self.v["label1"].get_text())

if __name__ == "__main__":
    unittest.main()
