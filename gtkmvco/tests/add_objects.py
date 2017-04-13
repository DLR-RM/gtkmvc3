import gtk

F = "adapter20.ui"
b = gtk.Builder()

# String instead of sequence argument silently fails
assert 1 == b.add_objects_from_file(F, "store")
assert not b.get_objects()

# Only a warning when loading without dependencies
assert 1 == b.add_objects_from_file(F, ["window1"])
assert b.get_objects()

# We could show the window now, but the spinner wouldn't work

print "If you can read this, GtkBuilder has terrible error handling"
