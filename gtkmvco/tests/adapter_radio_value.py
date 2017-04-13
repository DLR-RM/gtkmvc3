import _importer
from gtkmvc import Model, View, Controller
import gtk

# Shows how a group of radio actions can be adapted to a
# unique OP. The integer value of the OP is the value of the
# actions. The setting is bi-directional, but to set the
# active radio the exacct match is required, or the radio is not set.
#
# Since the default adapter for RadioAction adapts the label,
# 'flavour' is used when adapting, to select the default adapters
# which uses the value instead.

class MyModel (Model):

    val = 0
    __observables__ = ("val",)
    pass

class MyViewActions (View):
    builder = "adapter_radio_actions.glade"
    top = "window1"

    def __init__(self):
        View.__init__(self)

        # sets the rb active state
        self["rb1"].set_active(True)
        for name in "rb2 rb3 rb4".split(): self[name].set_active(False)
        return
    pass

class MyCtrl (Controller):

    def register_view(self, view):
        view['window1'].connect("delete-event", lambda x,e: gtk.main_quit())
        return

    def register_adapters(self):
        for i in range(1, 5): self.adapt("val", "rb%d" % i, flavour="value")

        # this is used to show the current value
        self.adapt("val", "entry_value")
        return

    @Controller.observe("val", assign=True)
    def val_notify(self, model, name, info):
        print "Notify change", name, model, model.val, type(model.val)
        return

    pass # end of class


m = MyModel()

# enable these to use radio actions:
v2 = MyViewActions()
c2 = MyCtrl(m, v2)

gtk.main()

