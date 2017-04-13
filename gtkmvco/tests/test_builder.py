import unittest

import gtk

from _importer import refresh_gui

import gtkmvc

class Model(gtkmvc.Model):
    label1 = 0
    label2 = 0
    __observables__ = ['label[12]']

class First(gtkmvc.Controller):
    def register_adapters(self):
        self.adapt('label1')

    def on_button1_clicked(self, widget):
        self.model.label1 += 1

class Second(gtkmvc.Controller):
    def register_adapters(self):
        self.adapt('label2')
        self.event = False

    def on_button2_clicked(self, widget):
        self.model.label2 += 1

    def on_button1_clicked(self, widget):
        self.event = True

class ConcurrentControllers(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(builder="test_builder.glade", top="window1")
        self.c = First(self.m, self.v)
        self.d = Second(self.m, self.v)
        refresh_gui()

    def testFirst(self):
        self.v['button1'].clicked()
        self.assertEquals(1, self.m.label1)
        self.assertEquals('1', self.v['label1'].get_text())

    def testSecond(self):
        self.v['button2'].clicked()
        self.assertEquals(1, self.m.label2)
        self.assertEquals('1', self.v['label2'].get_text())

    def testConcurrent(self):
        self.v['button1'].clicked()
        self.assertTrue(self.d.event)

if __name__ == "__main__":
    unittest.main()
