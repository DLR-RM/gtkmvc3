import unittest

import gtk

from _importer import refresh_gui

import gtkmvc

class Model(gtkmvc.Model):
    title = ''
    __observables__ = ['title']

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view['window'] = gtk.Window()

    def register_adapters(self):
        self.adapt('title', 'window', 'title')

class PropertyAdapter(unittest.TestCase):
    def testConnection(self):
        m = Model()
        v = gtkmvc.View()
        c = Controller(m, v)
        refresh_gui()
        self.assertEqual(m.title, v['window'].get_title())
        m.title = "Hello"
        self.assertEqual(m.title, v['window'].get_title())
        v['window'].set_title("World")
        self.assertEqual(m.title, v['window'].get_title())

if __name__ == '__main__':
    unittest.main()
