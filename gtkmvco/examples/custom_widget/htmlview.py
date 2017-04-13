"""
Program should show some rendered HTML. Clicking the link should open your
browser. Closing the window should exit the program.

This demonstrates the GtkBuilder way to easily use custom widget subclasses.
"""
import webbrowser

import gtk

import _importer
import gtkmvc
# We have to import it manually to make the gtype known, or Builder will raise.
# This is taken unchanged from http://people.gnome.org/~gjc/htmltextview.py
import htmltextview

# There is no multi-line lambda.
def setter(w, v):
    # clear
    w.set_buffer(gtk.TextBuffer())
    w.display_html(v)

gtkmvc.adapters.default.add_adapter(htmltextview.HtmlTextView,
    None, None, setter, str)

class Model(gtkmvc.Model):
    markup = """
        <body xmlns='http://www.w3.org/1999/xhtml'>
          <p style='text-align:center'>Hey, are you licensed to <a href='http://www.jabber.org/'>Jabber</a>?</p>
          <ul style='background-color:rgb(120,140,100)'>
           <li> One </li>
           <li> Two </li>
           <li> Three </li>
          </ul>
        </body>
        """
    __observables__ = ("markup",)

class View(gtkmvc.View):
    # Notice the following line in that file:
    # <!-- interface-requires pygtkmvc -->
    # To edit it export GLADE_CATALOG_PATH=examples/custom_widget
    builder = "htmlview.ui"
    top = "window"

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view.get_top_widget().connect("delete-event", gtk.main_quit)
        view["htmlview"].connect("url-clicked", self.navigate)

    def register_adapters(self):
        self.adapt("markup", "htmlview")

    def navigate(self, textview, url, linktype):
        webbrowser.open(url)

m = Model()
v = View()
c = Controller(m, v)

gtk.main()
