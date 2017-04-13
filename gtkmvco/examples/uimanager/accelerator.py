"""
To make shortcuts work both AccelMap and AccelGroup have to know about them.
"""

import gtk

key, mod = gtk.accelerator_parse("<ctrl>s")
assert gtk.accelerator_valid(key, mod)
PATH = "<MyApp-MainWindow>/Save"
gtk.accel_map_add_entry(PATH, key, mod)

group = gtk.AccelGroup()
group.connect_by_path(PATH, gtk.main_quit)

window = gtk.Window()
assert not gtk.accel_groups_from_object(window)
window.add_accel_group(group)

window.show_all()
gtk.main()
