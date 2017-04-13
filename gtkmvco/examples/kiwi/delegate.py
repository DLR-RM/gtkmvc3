import _importer

from gtkmvc import Model, View, Controller
import gtk, logging


"""
# This is the original kiwi's code
#!/usr/bin/env python
import gtk

from kiwi.ui.delegates import Delegate

class Farenheit(Delegate):
    widgets = ["quitbutton", "temperature", "celsius", "farenheit",
               "celsius_label" , "farenheit_label", "temperature_label"]
    gladefile = "faren"
    def __init__(self):
        Delegate.__init__(self, delete_handler=self.quit_if_last)

    def convert_temperature(self, temp):
        farenheit = (temp * 9/5.0) + 32
        celsius = (temp - 32) * 5/9.0
        return farenheit, celsius

    def clear_temperature(self):
        self.farenheit.set_text("")
        self.celsius.set_text("")

    # Signal handlers

    def on_quitbutton__clicked(self, *args):
        self.hide_and_quit()

    def after_temperature__changed(self, entry, *args):
        temp = entry.get_text().strip() or None
        if temp is None:
            self.clear_temperature()
        else:
            try:
                farenheit, celsius = self.convert_temperature(float(temp))
            except ValueError:
                farenheit = celsius = float('nan')
            self.farenheit.set_text("%.2f" % farenheit)
            self.celsius.set_text("%.2f" % celsius)

delegate = Farenheit()
delegate.show()
gtk.main()
"""

# This is the same example written with gtkmvc (requires 1.99.2)
class MyModel (Model):
    temperature = 0.0
    __observables__ = ("temperature", "celsius", "fahrenheit")

    @Model.getter(deps=["temperature"])
    def celsius(self): return (self.temperature - 32) * 5/9.0

    @Model.getter(deps=["temperature"])
    def fahrenheit(self): return (self.temperature * 9/5.0) + 32
    pass # end of class

class MyController (Controller):
    def on_window1__delete_event(self, w, e): gtk.main_quit()
    def on_button_quit__clicked(self, b): gtk.main_quit()
    pass

m = MyModel()
v = View(builder="delegate.glade")
c = MyController(m, v, auto_adapt=True, handlers="class")
gtk.main()

    


