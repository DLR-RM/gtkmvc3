"""
Actions are easiest to set up in code.
"""

import gtk

actiongroup = gtk.ActionGroup("MainWindow")
actiongroup.add_actions([
    ("file", None, "File"),
    ("save", gtk.STOCK_SAVE, "Save", "<ctrl>s", "saves the current file",
        gtk.main_quit),
    ])

manager = gtk.UIManager()
manager.add_ui_from_file("managed.xml")
manager.insert_action_group(actiongroup)

window = gtk.Window()
window.add_accel_group(manager.get_accel_group())

window.show_all()
gtk.main()
