import time

import gtk

# https://sourceforge.net/apps/trac/pygtkmvc/ticket/46
def RadioAction__notify_current_value(widget, handler, *args):
    """
    With GTK 2.22.1 the first time a group of RadioButton changes neither
    changed nor notify::current-value are emitted:
    https://bugzilla.gnome.org/show_bug.cgi?id=615458

    We work around this by using the toggled signal. Unfortunately this is
    emitted twice per button per change:
    http://faq.pygtk.org/index.py?req=show&file=faq09.004.htp

    Also during the first emission both the old and the new selected button
    have their active property set.
    We use this to filter out the first emission and call the real handler
    on the second one.

    Unlike the notify signal, toggled is emitted even if the active button is
    just clicked again. Since the handler is probably an Adapter, and filters
    out spurious notifications, we don't work around that here.

    More severly, it is impossible to instantiate gobject.GParamSpec in
    Python, so we just pass None as the second argument. Again this doesn't
    matter for Adapter.
    """
    group = widget.get_group() or [widget]
    active = [action for action in group if action.get_active()]
    if len(active) == 1:
        handler(widget, None, *args)

# https://sourceforge.net/apps/trac/pygtkmvc/ticket/50
def connect(widget, signal, handler, *args):
    """
    Use this instead of *widget*.connect if you want GTKMVC to
    automatically work around some known GTK bugs.
    """
    if (isinstance(widget, gtk.RadioAction) and
        signal == "notify::current-value"):
        widget.connect(
            "toggled", RadioAction__notify_current_value, handler, *args)
    else:
        widget.connect(signal, handler, *args)

def debug(gobject, property_spec, user_param):
    print time.time(), user_param, gobject.get_property("current-value")

builder = gtk.Builder()
builder.add_from_file("radio.ui")

for name in ('radioaction1', 'radioaction2'):
    builder.get_object(name).connect("notify::current-value", debug, "raw")
    connect(builder.get_object(name), "notify::current-value", debug, "fix")

builder.get_object('window1').show_all()
gtk.main()
