import ctypes
import locale

try:
    from gtk import glade
except ImportError:
    GLADE = False
else:
    GLADE = True

import otool

def library():
    from gtk import _gtk
    for path in otool.libraries(_gtk.__file__):
        if "intl" in path:
            return path

def bindtextdomain(*args):
    if hasattr(locale, "bindtextdomain"):
        locale.bindtextdomain(*args)
    elif GLADE:
        glade.bindtextdomain(*args)
    elif otool.exists():  # Could use lsof instead
        intl = ctypes.CDLL(library())
        intl.bindtextdomain(*args)
    # On Windows you also need ctypes, see TransUtils.py in
    # http://gramps-project.org
    #
    # Gramps also has MacTransUtils.py to determine the preferred language
    # if the environment variables are missing.
    # On Windows this can probably done with
    # https://launchpad.net/gettext-py-windows
    #
    # It may also be necessary to set the character set, but as GTK expects
    # UTF-8 and my .po files are that I didn't see problems so far.
