## Copyright (C) 2009 Roberto Cavada

import _importer

from gtkmvc import Model
from gtkmvc import View
from gtkmvc import Controller

import gtk

class MyView (View):
    glade = "example.glade"
    top = "window1"

    def enable_rb2(self, flag):
        """enables/disables all widgets regarding rb2"""
        self['table1'].set_sensitive(flag)
        return

    pass  # end of class


class MyModel(Model):
    use_rb1 = True
    option1 = 5
    option2 = "text for option2"

    __observables__ = ("use_rb1", "option1", "option2")

    def do_action(self):
        print "model performs action:", \
            self.use_rb1, self.option1, self.option2
        return

    pass  # end of class


class MyController(Controller):

    def register_view(self, view):
        return

    def register_adapters(self):
        self.adapt("use_rb1", "rb1")
        self.adapt("option1")
        self.adapt("option2")
        return

    # signals handling
    def on_button_action_clicked(self, button):
        self.model.do_action()
        return

    def on_window1_delete_event(self, w, e):
        gtk.main_quit()
        return False

    # observable properties notifications
    def property_use_rb1_value_change(self, model, old, new):
        self.view.enable_rb2(not new)
        return

    pass  # end of class


m = MyModel()
v = MyView()
c = MyController(m, v)
gtk.main()
