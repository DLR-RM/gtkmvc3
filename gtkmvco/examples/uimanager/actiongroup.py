"""
ActionGroup can assign accelerator path to Action.
"""

import gtk

action = gtk.Action("save", "Save", "saves the current file", gtk.STOCK_SAVE)
action.connect("activate", gtk.main_quit)
assert not action.get_accel_path()

actiongroup = gtk.ActionGroup("MainWindow")
actiongroup.add_action_with_accel(action, "<ctrl>s")
assert action.get_accel_path() == "<Actions>/MainWindow/save"

group = gtk.AccelGroup()

window = gtk.Window()
window.add_accel_group(group)

action.set_accel_group(group)
action.connect_accelerator()

window.show_all()
gtk.main()
