'''
#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class AboutDialog(Gtk.AboutDialog):
    def __init__(self):
        logo = None

        Gtk.AboutDialog.__init__(self)
        self.set_title("AboutDialog")
        self.set_name("Programmica")
        self.set_version("1.0")
        self.set_comments("Programming, system and network administration resources")
        self.set_website("https://programmica.com/")
        self.set_website_label("Programmica Website")
        self.set_authors(["Andrew Steele"])
        self.set_logo(logo)
        self.connect("response", self.on_response)

    def on_response(self, dialog, response):
        self.destroy()

aboutdialog = AboutDialog()
aboutdialog.run()
'''

'''
#!/usr/bin/env python
import gi
import socket
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

class Assistant(Gtk.Assistant):
    def __init__(self):
        Gtk.Assistant.__init__(self)
        self.incorrect_count = 0
        self.set_title("Assistant")
        self.set_default_size(600, -1)
        self.connect("cancel", self.on_cancel_clicked)
        self.connect("close", self.on_close_clicked)
        self.connect("apply", self.on_apply_clicked)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.append_page(self.box)
        self.set_page_type(self.box, Gtk.AssistantPageType.INTRO)
        self.hbox_connection_and_spinner = Gtk.Box(homogeneous=False)
        self.set_page_title(self.box, "Checking Internet Connection")
        self.label_checkingconnection = Gtk.Label("Please Wait While Checking Your Internet Connection")
        self.label_checkingconnection.set_line_wrap(True)
        self.connection_spinner = Gtk.Spinner()
        self.connection_spinner.start()
        self.hbox_connection_and_spinner.pack_start(self.label_checkingconnection, True, True, 0)
        self.hbox_connection_and_spinner.pack_start(self.connection_spinner, False, False, 0)
        self.label_noconnection = Gtk.Label("Please ensure that you are connected to the Internet before proceeding ")
        self.box.pack_start(self.hbox_connection_and_spinner, True, True, 0)
        self.box.pack_start(self.label_noconnection, False, False, 0)
        self.box.connect("show", self.allow_proceeding_further_for_key)

        self.box_license = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.append_page(self.box_license)
        self.set_page_type(self.box_license, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(self.box_license, "Enter License Key")
        label = Gtk.Label()
        label.set_markup(
            "<span font = \"Calibri 12\" >Please enter the license key provided to you</span>")
        label.set_line_wrap(True)
        self.hbox_license_entry_and_check_button = Gtk.Box(homogeneous=False, spacing=6)
        self.license_entry = Gtk.Entry()
        self.license_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
                                           "dialog-password")
        self.check_button = Gtk.Button("Check")
        self.check_button.connect("clicked", self.allow_proceeding_further_for_EULA)

        self.hbox_license_entry_and_check_button.pack_start(self.license_entry, True, True, 0)
        self.hbox_license_entry_and_check_button.pack_start(self.check_button, False, False, 0)

        self.box_license.pack_start(label, True, True, 0)
        self.box_license.pack_start(self.hbox_license_entry_and_check_button, False, False, 0)

        self.complete = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(self.complete)
        self.set_page_type(self.complete, Gtk.AssistantPageType.PROGRESS)
        self.set_page_title(self.complete, "End User License Agreement")
        self.scrollview_for_terms = Gtk.ScrolledWindow()
        self.label_terms = Gtk.Label(l)
        self.label_terms.set_line_wrap(True)
        self.scrollview_for_terms.add(self.label_terms)
        self.complete.pack_start(self.scrollview_for_terms, True, True, 0)
        checkbutton = Gtk.CheckButton(label="I accept the terms in license agreement")
        checkbutton.connect("toggled", self.on_complete_toggled)
        self.complete.pack_start(checkbutton, False, False, 0)

        self.box_summary = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(self.box_summary)
        self.set_page_type(self.box_summary, Gtk.AssistantPageType.SUMMARY)
        self.set_page_title(self.box_summary, "Finish Setup")
        label = Gtk.Label(label="All Set! You are ready to use the software")
        label.set_line_wrap(True)
        self.box_summary.pack_start(label, True, True, 0)
        self.set_page_complete(self.box_summary, True)

    def on_apply_clicked(self, *args):
        print("The 'Apply' button has been clicked")

    def on_close_clicked(self, *args):
        print("The 'Close' button has been clicked")
        Gtk.main_quit()

    def on_cancel_clicked(self, *args):
        print("The Assistant has been cancelled.")
        Gtk.main_quit()

    def on_complete_toggled(self, checkbutton):
        assistant.set_page_complete(self.complete, checkbutton.get_active())

    def allow_proceeding_further_for_key(self, widget):
        if is_connected():

            self.label_noconnection.hide()
            self.label_checkingconnection.set_text("You are connected to the internet! Proceed to continue")
            self.connection_spinner.stop()
            self.set_page_complete(self.box, True)
        else:
            self.label_noconnection.show()
            self.set_page_complete(self.box, False)

    def allow_proceeding_further_for_EULA(self, widget):
        self.entered_key = self.license_entry.get_text().strip()

        if self.entered_key == "Pawan":
            self.set_page_complete(self.box_license, True)
            self.incorrect_count = 0
        else :
            self.incorrect_count += 1
            if self.incorrect_count <= 3:
                pass
            elif self.incorrect_count > 3:
                Gtk.main_quit()



assistant = Assistant()
assistant.show_all()

Gtk.main()
'''

'''
title = "Tree Model with Large Data"
description = """
Implementation of the Gtk.TreeModel interface to create a custom model.
The demo uses a fake data store (it is not backed by a Python list) and is for
the purpose of showing how to override the TreeModel interfaces virtual methods.
"""

from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gtk


class Model(GObject.Object, Gtk.TreeModel):
    columns_types = (str, str)
    item_count = 100000
    item_data = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        super(Model, self).__init__()

    def do_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY

    def do_get_n_columns(self):
        return len(self.columns_types)

    def do_get_column_type(self, n):
        return self.columns_types[n]

    def do_get_iter(self, path):
        # Return False and an empty iter when out of range
        index = path.get_indices()[0]
        if index < 0 or index >= self.item_count:
            return False, None

        it = Gtk.TreeIter()
        it.user_data = index
        return True, it

    def do_get_path(self, it):
        return Gtk.TreePath([it.user_data])

    def do_get_value(self, it, column):
        if column == 0:
            return str(it.user_data)
        elif column == 1:
            return self.item_data

    def do_iter_next(self, it):
        # Return False if there is not a next item
        next = it.user_data + 1
        if next >= self.item_count:
            return False

        # Set the iters data and return True
        it.user_data = next
        return True

    def do_iter_previous(self, it):
        prev = it.user_data - 1
        if prev < 0:
            return False

        it.user_data = prev
        return True

    def do_iter_children(self, parent):
        # If parent is None return the first item
        if parent is None:
            it = Gtk.TreeIter()
            it.user_data = 0
            return True, it
        return False, None

    def do_iter_has_child(self, it):
        return it is None

    def do_iter_n_children(self, it):
        # If iter is None, return the number of top level nodes
        if it is None:
            return self.item_count
        return 0

    def do_iter_nth_child(self, parent, n):
        if parent is not None or n >= self.item_count:
            return False, None
        elif parent is None:
            # If parent is None, return the nth iter
            it = Gtk.TreeIter()
            it.user_data = n
            return True, it

    def do_iter_parent(self, child):
        return False, None


def main(demoapp=None):
    model = Model()
    # Use fixed-height-mode to get better model load and display performance.
    view = Gtk.TreeView(fixed_height_mode=True, headers_visible=False)
    column = Gtk.TreeViewColumn()
    column.props.sizing = Gtk.TreeViewColumnSizing.FIXED

    renderer1 = Gtk.CellRendererText()
    renderer2 = Gtk.CellRendererText()
    column.pack_start(renderer1, expand=True)
    column.pack_start(renderer2, expand=True)
    column.add_attribute(renderer1, 'text', 0)
    column.add_attribute(renderer2, 'text', 1)
    view.append_column(column)

    scrolled = Gtk.ScrolledWindow()
    scrolled.add(view)

    window = Gtk.Window(title=title)
    window.set_size_request(480, 640)
    window.add(scrolled)
    window.show_all()
    GLib.timeout_add(10, lambda *args: view.set_model(model))
    return window


if __name__ == "__main__":
    window = main()
    window.connect('destroy', Gtk.main_quit)
    Gtk.main()
'''
class Employee:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'
        self.pay = pay

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'Employee', 60000)
Employee.__init__(emp_1, 'Pawan', 'Sharma', 10000)
emp_1 = Employee('Corey', 'Schafer', 50000)
print(emp_1.first)