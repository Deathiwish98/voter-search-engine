'''SELECT DISTINCT a.*
FROM ELEWARD a
INNER JOIN (
    SELECT address, MAX(age) AS Maxage
    FROM ELEWARD
    GROUP BY address
) b ON a.address = b.address AND a.age = b.Maxage


INSERT INTO ele_head ( `AC`, `PART_NO`, `SLNOINPART`, `FM_NAME_V`, `RLN_FM_NAME_V`, `SEX`, `Age`, `ADDRESS`, `PSTATION`, `IDCARD_NO`)
SELECT * FROM ELEWARD
EXCEPT
SELECT * FROM HOF;

CREATE TABLE "ele_head" ( `AC` TEXT, `PART_NO` TEXT, `SLNOINPART` TEXT, `FM_NAME_V` TEXT, `RLN_FM_NAME_V` TEXT, `SEX` TEXT, `Age` TEXT, `ADDRESS` TEXT, `PSTATION` TEXT, `IDCARD_NO` TEXT )

SELECT count(*) FROM ELEWARD
where IDCARD_NO
not in (SELECT IDCARD_NO FROM HOF);

select * from ELEWARD
where IDCARD_NO in (
select IDCARD_NO FROM ELEWARD
group by 1
having count(1) > 1
)


'''

'''
import socket
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
print (is_connected())
'''

"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TreeModelSort(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, -1)
        self.connect("destroy", Gtk.main_quit)

        liststore = Gtk.ListStore(str)
        liststore.append(["Mark"])
        liststore.append(["Chris"])
        liststore.append(["Tim"])
        liststore.append(["David"])
        liststore.append(["Keith"])

        treemodelsort = Gtk.TreeModelSort(liststore)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_model(treemodelsort)
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)

window = TreeModelSort()
window.show_all()

Gtk.main()
"""

'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TreeStore(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, -1)
        self.connect("destroy", Gtk.main_quit)

        treestore = Gtk.TreeStore(str, str)
        dog = treestore.append(None, ["Dog","ABCD"])
        treestore.append(dog, ["Fido","a"])
        treestore.append(dog, ["Spot","b"])
        cat = treestore.append(None, ["Cat","EFGH"])
        treestore.append(cat, ["Ginger","c"])
        rabbit = treestore.append(None, ["Rabbit","IJKL"])
        treestore.append(rabbit, ["Twitch","d"])
        treestore.append(rabbit, ["Floppy","e"])

        treeview = Gtk.TreeView()
        treeview.set_model(treestore)
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Pet Names")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

        treeviewcolumn = Gtk.TreeViewColumn("Alphabet")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)

window = TreeStore()
window.show_all()

Gtk.main()
'''

'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World Printing")
        self.button = Gtk.Button(label="Print A Rectangle")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        pd = Gtk.PrintOperation()
        pd.set_n_pages(1)
        pd.connect("draw_page", self.draw_page)
        result = pd.run(
            Gtk.PrintOperationAction.PRINT_DIALOG, None)
        print (result)  # handle errors etc.

    def draw_page(self, operation=None, context=None, page_nr=None):
        ctx = context.get_cairo_context()
        w = context.get_width()
        h = context.get_height()
        ctx.set_source_rgb(0.5, 0.5, 1)
        ctx.rectangle(w*0.1, h*0.1, w*0.8, h*0.8)
        ctx.stroke()
        return

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
'''

'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class EntryWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Entry Demo")
        self.set_size_request(200, 100)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.check_editable = Gtk.CheckButton("Editable")
        self.check_editable.connect("toggled", self.on_editable_toggled)
        self.check_editable.set_active(True)
        hbox.pack_start(self.check_editable, True, True, 0)

        self.check_visible = Gtk.CheckButton("Visible")
        self.check_visible.connect("toggled", self.on_visible_toggled)
        self.check_visible.set_active(True)
        hbox.pack_start(self.check_visible, True, True, 0)

        self.pulse = Gtk.CheckButton("Pulse")
        self.pulse.connect("toggled", self.on_pulse_toggled)
        self.pulse.set_active(False)
        hbox.pack_start(self.pulse, True, True, 0)

        self.icon = Gtk.CheckButton("Icon")
        self.icon.connect("toggled", self.on_icon_toggled)
        self.icon.set_active(False)
        hbox.pack_start(self.icon, True, True, 0)

    def on_editable_toggled(self, button):
        value = button.get_active()
        self.entry.set_editable(value)

    def on_visible_toggled(self, button):
        value = button.get_active()
        self.entry.set_visibility(value)

    def on_pulse_toggled(self, button):
        if button.get_active():
            self.entry.set_progress_pulse_step(0.2)
            # Call self.do_pulse every 100 ms
            self.timeout_id = GObject.timeout_add(100, self.do_pulse, None)
        else:
            # Don't call self.do_pulse anymore
            GObject.source_remove(self.timeout_id)
            self.timeout_id = None
            self.entry.set_progress_pulse_step(0)

    def do_pulse(self, user_data):
        self.entry.progress_pulse()
        return True

    def on_icon_toggled(self, button):
        if button.get_active():
            icon_name = "dialog-password"
        else:
            icon_name = None
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
                                           icon_name)


win = EntryWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
'''

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

WINDOW_WIDTH, WINDOW_HEIGHT = 150, 100

class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="HeaderBar Demo")


        #self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.canvas = Gtk.HBox()

        button = Gtk.Button("Hello World!")
        button.connect("clicked", self.abcd)
        self.canvas.add(button)

        self.add(self.canvas)


    def abcd(self, widget):
        window = Gtk.OffscreenWindow()
        #window.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        window.show()

        original_parent = self.canvas.get_parent()
        self.canvas.reparent(window)

        while Gtk.events_pending():
            Gtk.main_iteration()

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                  WINDOW_WIDTH, WINDOW_HEIGHT)

        cr = cairo.Context(surf)
        self.canvas.draw(cr)
        surf.write_to_png('test.png')

        self.canvas.reparent(original_parent)




abc = HeaderBarWindow()

abc.show_all()
Gtk.main()




'''
# this is needed, otherwise the screenshot is black:
while Gtk.events_pending():
    Gtk.main_iteration()

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                          WINDOW_WIDTH, WINDOW_HEIGHT)

cr = cairo.Context(surf)
canvas.draw(cr)
surf.write_to_png('test.png')
'''