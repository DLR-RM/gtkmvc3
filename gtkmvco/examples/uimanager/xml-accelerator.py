import gtk

actiongroup = gtk.ActionGroup("MainWindow")
actiongroup.add_actions([
    ("save", None, "Save", None, "saves the current file",
        gtk.main_quit),
    ])
print actiongroup.get_action("save").get_accel_path()

def debug(*args):
    print args
gtk.accel_map_foreach(debug)

manager = gtk.UIManager()
manager.insert_action_group(actiongroup)
manager.add_ui_from_string("""
<ui>
	<accelerator action="save"/>
</ui>
""")
gtk.accel_map_foreach(debug)

gtk.main()
