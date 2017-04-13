"""
# Create red.ui.h because xgettext doesn't understand XML
$ intltool-extract --type=gettext/glade red.ui
# Collect strings from source code and UI
$ xgettext --language=Python --keyword=_ --keyword=N_ --output=red.pot red.py red.ui.h
# Start translation from template
$ msginit --input=red.pot --locale=de_DE
# Create proper location
$ mkdir -p de_DE/LC_MESSAGES
# Convert to runtime format (machine dependent!)
$ msgfmt --output-file=de_DE/LC_MESSAGES/red.mo de.po
"""

import gettext

import gtk

import translation

def handler(widget):
    print _("Yellow")

translation.bindtextdomain("red", "./")  # Only affects GtkBuilder
gettext.install("red", "./")  # Only affects _()

builder = gtk.Builder()
# This is an alternative to <interface domain="red"> in the XML beacuse
# currently Glade will remove that on save.
# https://bugzilla.gnome.org/show_bug.cgi?id=669002
builder.set_translation_domain("red")
builder.add_from_file("red.ui")

window = builder.get_object("window")
window.show_all()
button = builder.get_object("button")
button.connect("clicked", handler)

gtk.main()
