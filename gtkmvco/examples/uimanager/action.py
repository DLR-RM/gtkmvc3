"""
Action can tell AccelGroup about shortcuts.
"""

import gtk

key, mod = gtk.accelerator_parse("<ctrl>s")
PATH = "<MyApp-MainWindow>/Save"
gtk.accel_map_add_entry(PATH, key, mod)

group = gtk.AccelGroup()

window = gtk.Window()
window.add_accel_group(group)

action = gtk.Action("save", "Save", "saves the current file", gtk.STOCK_SAVE)
action.connect("activate", gtk.main_quit)
action.set_accel_path(PATH)
action.set_accel_group(group)
action.connect_accelerator()

window.show_all()
gtk.main()
