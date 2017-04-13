"""
Get Action from Glade but set shortcut in code.
This avoids manually setting accelerator paths.
"""

import gtk

builder = gtk.Builder()
builder.add_from_file("managed.ui")

actiongroup = gtk.ActionGroup("MainWindow")
actiongroup.add_action(builder.get_object("file"))
action = builder.get_object("save")
action.connect("activate", gtk.main_quit)

actiongroup.add_action_with_accel(action, "<ctrl>s")

manager = gtk.UIManager()
manager.insert_action_group(actiongroup)
manager.add_ui_from_file("managed.xml")

window = gtk.Window()
window.add_accel_group(manager.get_accel_group())

window.show_all()
gtk.main()
