"""
Get all Action-related objects from a recent version of Glade.
"""

import gtk

builder = gtk.Builder()
builder.add_from_file("actiongroup.ui")

builder.get_object("save").connect("activate", gtk.main_quit)

manager = gtk.UIManager()
manager.insert_action_group(builder.get_object("actiongroup"))
manager.add_ui_from_file("managed.xml")

window = gtk.Window()
window.add_accel_group(manager.get_accel_group())

bar = manager.get_widget("/menubar")
window.add(bar)

window.show_all()
gtk.main()
