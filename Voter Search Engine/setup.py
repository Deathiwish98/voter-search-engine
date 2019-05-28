import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Fixed(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Fixed")

        self.set_default_size(200, 200)
        self.connect("destroy", Gtk.main_quit)

        fixed = Gtk.Fixed()
        self.add(fixed)

        self.button = Gtk.Label(label="Button 1")
        fixed.put(self.button, 0, 0)
        self.button2 = Gtk.Button(label="Button 2")
        fixed.put(self.button2, 120, 95)
        self.button2.set_size_request(self.button.get_allocation().width * 3,
                                        self.button.get_allocation().height * 3)

window = Fixed()
window.show_all()
print(window.button.get_allocation().width)
window.button2.set_size_request(window.button.get_allocation().width*3, window.button.get_allocation().height*3)

Gtk.main()