import gi
import sqlite3
import cairo
import re
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GObject


Screensize = Gdk.Screen.get_default()
ScreenHeight = Screensize.get_height()
ScreenWidth = Screensize.get_width()

configurations = open("config.cfg", "r")
configurations = "".join(configurations.readlines())

path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

pattern_ac_name = re.compile(r'name_AC\s=\s"([\d\w-]+)"\s?')
ac_name = pattern_ac_name.search(configurations).group(1)
print(ac_name)

class VoterList(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Voter Slip")
        hb = Gtk.HeaderBar(title="Voter Slip")
        hb.set_show_close_button(True)
        self.set_titlebar(hb)
        self.set_resizable(False)

        self.button_popover = Gtk.Button()
        icon = Gio.ThemedIcon(name="applications-accessories")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_popover.add(image)
        self.button_popover.connect("clicked", self.open_popover)
        hb.pack_start(self.button_popover)

        self.popover_menu = Gtk.PopoverMenu.new()
        self.popover_menu.set_relative_to(self.button_popover)

        self.popoverbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.popover_menu.add(self.popoverbox)

        self.Save_vlist = Gtk.ModelButton("Save")
        self.Save_vlist.set_property('margin', 10)
        self.popoverbox.pack_start(self.Save_vlist, False, False, 0)
        self.Save_vlist.connect("clicked", self.Save_voter_slip)

        self.exit_btn = Gtk.ModelButton("Exit")
        self.popoverbox.pack_start(self.exit_btn, False, False, 0)
        self.exit_btn.set_property('margin', 10)
        self.exit_btn.connect("clicked", lambda x : self.destroy())

        self.set_size_request(1, 1)
        self.Vbox_voter_slip = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.Hbox_voter_slip = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=False)
        self.Frame_voter_slip_generator = Gtk.Frame()
        # self.Vbox_voter_slip.pack_start(self.Hbox_voter_slip, False, False, 0)
        self.Vbox_voter_slip.set_center_widget(self.Hbox_voter_slip)
        self.Hbox_voter_slip.set_center_widget(self.Frame_voter_slip_generator)
        self.Frame_voter_slip_generator.set_size_request(5, 5)
        self.fixed_voter_slip = Gtk.Fixed()
        self.Frame_voter_slip_generator.add(self.fixed_voter_slip)
        self.result = list(map(list, win.result))[0]

        self.label_ac_name = Gtk.Label()
        self.label_ac_name.set_markup(
            "<span font = \"Calibri 12\" >{}</span>".format(ac_name))
        self.fixed_voter_slip.put(self.label_ac_name, 142, 2)

        self.seperator_for_slip_ac = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.seperator_for_slip_ac.set_size_request(360, 0)
        self.fixed_voter_slip.put(self.seperator_for_slip_ac, 3, 20)

        self.label_slip_sr_no = Gtk.Label()
        self.label_slip_sr_no.set_markup("<span font = \"DV-TTYogesh 14\" >G¨É ºÉÆJªÉÉ :</span>")
        self.fixed_voter_slip.put(self.label_slip_sr_no, 3, 20)
        self.dlabel_slip_sr_no = Gtk.Label()
        self.dlabel_slip_sr_no.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[2]))
        self.fixed_voter_slip.put(self.dlabel_slip_sr_no, 70, 22)

        self.label_slip_name = Gtk.Label()
        self.label_slip_name.set_markup("<span font = \"DV-TTYogesh 14\" >xÉÉ¨É:</span>")
        self.fixed_voter_slip.put(self.label_slip_name, 3, 38)
        self.dlabel_slip_name = Gtk.Label()
        self.dlabel_slip_name.set_markup("<span font = \"Calibri Bold 11\" >{}</span>".format(self.result[3]))
        self.fixed_voter_slip.put(self.dlabel_slip_name, 33, 40)

        self.label_slip_age = Gtk.Label()
        self.label_slip_age.set_markup("<span font = \"DV-TTYogesh 14\" >+ÉªÉÖ:</span>")
        self.fixed_voter_slip.put(self.label_slip_age, 204, 20)
        self.dlabel_slip_age = Gtk.Label()
        self.dlabel_slip_age.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[6]))
        self.fixed_voter_slip.put(self.dlabel_slip_age, 232, 22)

        self.label_slip_part_no = Gtk.Label()
        self.label_slip_part_no.set_markup("<span font = \"DV-TTYogesh 14\" >¦ÉÉMÉ ºÉÆJªÉÉ:</span>")
        self.fixed_voter_slip.put(self.label_slip_part_no, 280, 20)
        self.dlabel_slip_part_no = Gtk.Label()
        self.dlabel_slip_part_no.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[1]))
        self.fixed_voter_slip.put(self.dlabel_slip_part_no, 348, 22)

        self.label_slip_sex = Gtk.Label()
        self.label_slip_sex.set_markup("<span font = \"DV-TTYogesh 14\" >Ë±ÉMÉ :</span>")
        self.fixed_voter_slip.put(self.label_slip_sex, 280, 40)
        self.dlabel_slip_sex = Gtk.Label()
        self.dlabel_slip_sex.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[5]))
        self.fixed_voter_slip.put(self.dlabel_slip_sex, 320, 42)

        self.dlabel_slip_idcard = Gtk.Label()
        self.dlabel_slip_idcard.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[9]))
        self.fixed_voter_slip.put(self.dlabel_slip_idcard, 280, 61)

        self.label_slip_rln_name = Gtk.Label()
        self.label_slip_rln_name.set_markup("<span font = \"DV-TTYogesh 14\" >Ê{ÉiÉÉ/{ÉÊiÉ: </span>")
        self.fixed_voter_slip.put(self.label_slip_rln_name, 3, 58)
        self.dlabel_slip_rln_name = Gtk.Label()
        self.dlabel_slip_rln_name.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[4]))
        self.fixed_voter_slip.put(self.dlabel_slip_rln_name, 60, 60)

        self.label_slip_address = Gtk.Label()
        self.label_slip_address.set_markup("<span font = \"DV-TTYogesh 14\" >{ÉiÉÉ:</span>")
        self.fixed_voter_slip.put(self.label_slip_address, 3, 76)
        self.dlabel_slip_address = Gtk.Label()
        if len(self.result[7]) > 49:
            self.result[7] = self.result[7][:49] + "\n" + self.result[7][49:]
        self.dlabel_slip_address.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[7]))
        self.fixed_voter_slip.put(self.dlabel_slip_address, 30, 77)

        self.label_slip_pstation = Gtk.Label()
        self.label_slip_pstation.set_markup("<span font = \"DV-TTYogesh 14\" >¨ÉiÉnùÉxÉ Eäòxpù :</span>")
        self.fixed_voter_slip.put(self.label_slip_pstation, 3, 101)
        self.dlabel_slip_pstation = Gtk.Label()
        if len(self.result[8]) > 45:
            self.result[8] = self.result[8][:45] + "\n" + self.result[8][45:]
        self.dlabel_slip_pstation.set_markup("<span font = \"Calibri 11\" >{}</span>".format(self.result[8]))
        self.fixed_voter_slip.put(self.dlabel_slip_pstation, 83, 98)

        self.seperator_for_info = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.seperator_for_info.set_size_request(360, 0)
        self.fixed_voter_slip.put(self.seperator_for_info, 3, 132)

        pattern_appeal = re.compile(r'appeal\s=\s"(.*?)"\s?')
        appeal = pattern_appeal.search(configurations).group(1)

        self.label_ac_info = Gtk.Label()
        self.label_ac_info.set_markup(
            "{}".format(appeal))
        self.fixed_voter_slip.put(self.label_ac_info, 15, 134)
        self.add(self.Vbox_voter_slip)
        self.show_all()
        del win.result[:]

    def open_popover(self, button):
        # Toggle
            if self.popover_menu.get_visible():
                self.popover_menu.hide()
            else:
                self.popover_menu.show_all()

    def Save_voter_slip(self, widget):
        window = Gtk.OffscreenWindow()
        #window.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        window.show()

        original_parent = self.Vbox_voter_slip.get_parent()
        self.Vbox_voter_slip.reparent(window)

        while Gtk.events_pending():
            Gtk.main_iteration()

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 370, 165)

        cr = cairo.Context(surf)
        self.Vbox_voter_slip.draw(cr)
        #surf.write_to_png(os.path.join(path_desktop, "{}.png".format(self.result[3] + "  " + self.result[9])))
        surf.write_to_png(os.path.join(path_desktop, "Voter_slip.png"))

        self.Vbox_voter_slip.reparent(original_parent)

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Search Results")
        self.maximize()
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scrollwindow_frame = Gtk.ScrolledWindow()
        self.add(self.layout)
        self.conn = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.cur = self.conn.cursor()
        self.combo_text = ""

        self.listfortreeview = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str)
        for item in win.result:
            self.listfortreeview.append(list(item))

        self.current_ps_filter = None

        self.ps_filter = self.listfortreeview.filter_new()
        self.ps_filter.set_visible_func(self.ps_filter_func)

        self.ps_filter_sorted = Gtk.TreeModelSort(model=self.ps_filter)

        self.votertreeview = Gtk.TreeView.new_with_model(self.ps_filter_sorted)
        self.votertreeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

        for i, coltitle in enumerate(["AC", "PART NO", "SR NO", "NAME", "RELATION'S NAME", "SEX", "AGE", "ADDRESS",
                                      "PSTATION", "IDCARD NO"]):
            # rendered = Gtk.CellRendererText(wrap_mode=0, wrap_width=1)
            rendered = Gtk.CellRendererText(foreground="black")
            column = Gtk.TreeViewColumn(coltitle, rendered, text=i)
            column.set_sort_column_id(i)
            self.votertreeview.append_column(column)

        self.votertreeview.get_column(1).set_max_width(60)
        self.votertreeview.get_column(2).set_max_width(45)
        self.votertreeview.get_column(5).set_max_width(32)
        self.votertreeview.get_column(6).set_max_width(32)
        # self.votertreeview.get_column(8).queue_resize()

        closebtn = Gtk.Button("Close")
        closebtn.connect("clicked", self.close_result_window)

        filter_options = ["PART NO", "WARD NO"]
        filter_combo = Gtk.ComboBoxText()
        filter_combo.set_entry_text_column(0)
        filter_combo.connect("changed", self.on_filter_combo_changed)
        for abc in filter_options:
            filter_combo.append_text(abc)

        self.filter_text = Gtk.Entry()

        self.btn_filter = Gtk.Button("Filter")
        self.btn_filter.connect("clicked", self.filter_btn_clicked)
        self.filter_allowed = self.btn_filter.get_sensitive()

        self.btn_reset = Gtk.Button("Reset")
        self.btn_reset.connect("clicked", self.reset_filter)

        self.text_Total_records = "Total Records : " + str(len(self.listfortreeview))
        self.label_total_records = Gtk.Label(self.text_Total_records, margin_end=5)
        self.label_Filtered_records = Gtk.Label(margin_end=5)

        self.hbox = Gtk.Box(homogeneous=False)
        self.hbox.pack_start(closebtn, False, False, 0)

        self.hbox_center = Gtk.Box(spacing=10)
        self.hbox_center.pack_start(Gtk.Label("Filter By:"), False, False, 5)
        self.hbox_center.pack_start(filter_combo, False, False, 0)
        self.hbox_center.pack_start(self.filter_text, False, False, 0)
        self.hbox_center.pack_start(self.btn_filter, False, False, 0)
        self.hbox_center.pack_start(self.btn_reset, False, False, 0)

        self.hbox.set_center_widget(self.hbox_center)
        self.hbox.pack_end(self.label_Filtered_records, False, False, 0)
        self.label_Filtered_records.hide()
        self.hbox.pack_end(self.label_total_records, False, False, 0)


        self.layout.pack_start(self.hbox, False, False, 0)
        self.layout.pack_start(scrollwindow_frame, True, True, 0)
        scrollwindow_frame.add(self.votertreeview)
        self.show_all()
        del win.result[:]

    def close_result_window(self, window):
        self.listfortreeview.clear()
        self.destroy()

    def ps_filter_func(self, model, iter, data):

            if self.current_ps_filter is None or self.current_ps_filter == "None":
                return True
            elif self.combo_text == "PART NO":
                return model[iter][1] == self.current_ps_filter

    def on_filter_combo_changed(self, combo):
        self.combo_text = combo.get_active_text()

        if self.combo_text == "PART NO":
            if self.btn_filter.get_sensitive() != True:
                self.btn_filter.set_sensitive(True)
        elif self.combo_text == "WARD NO":
            if self.btn_filter.get_sensitive() != False:
                self.btn_filter.set_sensitive(False)

    def filter_btn_clicked(self, button):
        self.get_typed_filter = self.filter_text.get_text().strip()
        if self.get_typed_filter == "":
            self.current_ps_filter = "None"
        else:
            self.current_ps_filter = self.get_typed_filter
        self.ps_filter.refilter()
        self.text_Filtered_records = "\tFiltered Records : " + str(len(self.ps_filter))
        self.label_Filtered_records.set_text(self.text_Filtered_records)
        self.label_Filtered_records.show()

    def reset_filter(self, button):
        self.current_ps_filter = "None"
        self.filter_text.set_text("")
        self.ps_filter.refilter()
        self.label_Filtered_records.hide()

    def add_label_filtered_records(self):
        if self.current_ps_filter != "None":
            list_of_children = self.hbox_center.get_children()
            if self.label_Filtered_records in list_of_children:
                pass
            else:
                self.hbox_center.pack_end(self.label_Filtered_records, False, False, 0)

class HofWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Search Results")
        self.maximize()
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scrollwindow_frame = Gtk.ScrolledWindow()
        self.add(layout)
        self.abc=[]
        self.connforchild = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.curforchild = self.connforchild.cursor()

        self.listfortreeview = Gtk.TreeStore(str, str, str, str, str, str, str, str, str, str)
        for item in win.result:
            xyz = list(item)
            Parent = self.listfortreeview.append(None, xyz)
            self.curforchild.execute("SELECT * FROM ele_head WHERE ADDRESS =?", (xyz[7],))
            self.resultchild = self.curforchild.fetchall()
            if self.resultchild != []:
                for row in self.resultchild:
                    row = ["{}".format(" " + " " + " " + element) for element in list(row)]
                    self.listfortreeview.append(Parent, row)
        self.curforchild.close()
        self.connforchild.close()

        self.votertreeview = Gtk.TreeView(self.listfortreeview)
        self.votertreeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

        for i, coltitle in enumerate(["AC", "PART NO", "SR NO", "NAME", "RELATION'S NAME", "SEX", "AGE", "ADDRESS",
                                      "PSTATION", "IDCARD NO"]):
            rendered = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(coltitle, rendered, text=i)
            column.set_sort_column_id(i)
            self.votertreeview.append_column(column)

        #self.votertreeview.get_column(8).set_max_width(20)
        #self.votertreeview.get_column(8).queue_resize()

        closebtn = Gtk.Button("Close")
        closebtn.connect("clicked", self.close_result_window)
        layout.pack_start(closebtn, False, False, 0)
        layout.pack_start(scrollwindow_frame, True, True, 0)
        scrollwindow_frame.add(self.votertreeview)
        self.show_all()
        del win.result[:]

    def close_result_window(self, window):
        self.listfortreeview.clear()
        self.destroy()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="")
        self.set_border_width(20)
        #self.set_default_size(430,800)
        self.set_size_request(ScreenWidth/1.3, ScreenHeight/1.05)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.connect("show", self.hide_stack_switcher)
        self.result = []
        #self.statusbar = Gtk.Statusbar()

        # self.css_provider = Gtk.CssProvider()
        # self.css_provider.load_from_path('FileStyle.css')
        hb = Gtk.HeaderBar(title = "Voter Search Engine")
        hb.set_show_close_button(True)
        hb.set_subtitle("Search Made Easy")
        self.set_titlebar(hb)

        self.button_popover = Gtk.Button()
        icon = Gio.ThemedIcon(name="applications-accessories")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_popover.add(image)
        self.button_popover.connect("clicked", self.open_popover)
        hb.pack_end(self.button_popover)

        self.popover_menu = Gtk.PopoverMenu.new()
        self.popover_menu.set_relative_to(self.button_popover)

        self.popoverbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.popover_menu.add(self.popoverbox)

        self.one = Gtk.ModelButton("About")
        label1 = Gtk.Label("About")
        label1.set_padding(10, 10)
        #self.one.add(label1)
        self.one.set_name("btn_one")
        self.one.set_property('margin', 10)
        self.popoverbox.pack_start(self.one, False, False, 0)


        self.two = Gtk.ModelButton("Exit")
        label2 = Gtk.Label("Exit")
        label2.set_padding(10, 10)
        #self.two.add(label2)
        self.two.set_name("btn_two")
        self.two.connect("clicked", Gtk.main_quit)
        self.popoverbox.pack_start(self.two, False, False, 0)
        self.two.set_property('margin', 10)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        button.connect("clicked", self.clear_frame)
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        # --------------------Upper Hbox Starts Here----------------------#
        self.RootVbox = Gtk.Box(homogeneous = False, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.RootVbox)

        self.Hbox_Upper = Gtk.Box(homogeneous = False)
        self.image_title = Gtk.Image()
        self.image_title.set_from_file('Header2.png')
        #self.label_title = Gtk.Label()
        #self.label_title.set_markup("<span font = \"Monotype Corsiva Bold 60\" foreground=\"#93c5e2\" underline = \"low\">Voter Search Engine</span>")
        self.Vbox_center = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,spacing = 0, homogeneous = False)
        self.Vbox_center.pack_start(self.image_title, False ,False ,0)
        self.Hbox_Upper.set_center_widget(self.Vbox_center)
        self.image_candidate = Gtk.Image()
        self.image_candidate.set_from_file('candidate.jpg')
        self.Vbox_regdetails = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.label_regto = Gtk.Label()
        self.label_regto.set_markup("<span font = \"Arial Italic 12\" foreground=\"black\" >Licensed To:</span>")
        self.label_candname = Gtk.Label()
        pattern_cand_name = re.compile(r'name_cand\s=\s"([\s\w.]+)"\s?')
        cand_name = pattern_cand_name.search(configurations).group(1)
        self.label_candname.set_markup("<span font = \"Arial Italic 12\" foreground=\"black\" >{}</span>".format(cand_name))
        self.label_Party = Gtk.Label()
        pattern_party_name = re.compile(r'name_party\s=\s"([\s\w.]+)"\s?')
        party_name = pattern_party_name.search(configurations).group(1)
        self.label_Party.set_markup("<span font = \"Arial Italic 12\" foreground=\"black\" >{}</span>".format(party_name))
        self.Hbox_Upper.pack_end(self.image_candidate, False, False, 5)
        self.Vbox_regdetails.pack_start(self.label_regto, False, True, 5)
        self.Vbox_regdetails.pack_start(self.label_candname, False, True, 5)
        self.Vbox_regdetails.pack_start(self.label_Party, False, True, 5)
        self.Hbox_Upper.pack_end(self.Vbox_regdetails, False, True, 20)

        self.RootVbox.pack_start(self.Hbox_Upper, False, False, 0)

        #----------------------------Upper Hbox Ends Here--------------------------#

        #----------------------------Lower Hbox Starts Here------------------------#
        self.Hbox_Lower = Gtk.Box(homogeneous=False)
        self.Revealer_stackbar = Gtk.Revealer()
        self.Revealer_stackbar.set_transition_type(2)
        self.Revealer_stackbar.set_transition_duration(1000)
        self.Revealer_stackbar.set_reveal_child(False)
        self.Hbox_Lower.pack_start(self.Revealer_stackbar, False, False, 0)

        #----------------------------Root Stack Stars Here-------------------------#
        self.root_stack = Gtk.Stack()
        self.root_stack.set_transition_type(9)
        self.root_stacksidebar = Gtk.StackSidebar()
        self.root_stacksidebar.set_size_request(200,100)
        self.root_stacksidebar.set_margin_top(15)
        self.root_stacksidebar.set_stack(self.root_stack)

        self.Revealer_stackbar.add(self.root_stacksidebar)

        #-----------------------------Lower Frame Starts Here----------------------#
        self.stack_middle = Gtk.Stack(homogeneous = False, interpolate_size=False)
        self.stack_middle.set_transition_type(14)
        self.stack_middle.set_transition_duration(1000)
        self.box_middleRootframe = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=True)
        self.stack_middle.add_named(self.box_middleRootframe, "Dashboard")

        #------------------------General Search Starts here-------------------------#

        self.label_constituency = Gtk.Label("Assembly Name", margin_start=0)
        self.label_name = Gtk.Label("Voter's Name", margin_start=0)
        self.label_rlnname = Gtk.Label("Relation's Name", margin_start=0)
        self.label_voterid = Gtk.Label("Voter ID Card No.", margin_start=0)
        self.entry_constituency = Gtk.Entry(text = "{}".format(ac_name), editable=False, margin_end=0)
        self.entry_name = Gtk.Entry(max_length=20, xalign=0, margin_end=0, can_focus=True)
        self.entry_rlnname = Gtk.Entry(margin_end=0)
        self.entry_voterid = Gtk.Entry(margin_end=0)
        for entry in [self.entry_name, self.entry_rlnname, self.entry_voterid]:
            entry.connect("activate", self.show_search_results_gen)
        self.Button_Submit = Gtk.Button("Submit")
        self.Button_Submit.set_name("btn_submit")
        self.Button_Submit.connect("clicked", self.show_search_results_gen)
        self.Button_Submit.connect("key-release-event", self.show_search_results_gen_enter)

        self.grid_gensearch = Gtk.Grid(row_spacing=15, column_homogeneous=True, row_homogeneous=False)
        self.grid_gensearch.attach(self.label_constituency, 0, 0, 1, 1)
        self.grid_gensearch.attach(self.entry_constituency, 2, 0, 1, 1)
        self.grid_gensearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 1, 3, 1)
        self.grid_gensearch.attach(self.label_name,0, 2, 1, 1)
        self.grid_gensearch.attach(self.entry_name, 2, 2, 1, 1)
        self.grid_gensearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 3, 3, 1)
        self.grid_gensearch.attach(self.label_rlnname, 0, 4, 1, 1)
        self.grid_gensearch.attach(self.entry_rlnname, 2, 4, 1, 1)
        self.grid_gensearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 5, 3, 1)
        self.grid_gensearch.attach(self.label_voterid, 0, 6, 1, 1)
        self.grid_gensearch.attach(self.entry_voterid, 2, 6, 1, 1)

        self.grid_gensearch.attach(self.Button_Submit, 1, 7, 1, 1)
        self.grid_gensearch.set_border_width(20)

        self.Frame_gensearch = Gtk.Frame(vexpand=False)
        self.Frame_gensearch.set_hexpand(False)
        self.Frame_gensearch.set_hexpand_set(False)
        self.Frame_gensearch.add(self.grid_gensearch)
        self.Frame_gensearch.set_border_width(0)


        self.Hbox_gensearch = Gtk.Box(homogeneous = False)
        self.Hbox_gensearch.set_center_widget(self.Frame_gensearch)

        self.Vbox_gensearch = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL)
        self.label_gentab_gensearch = Gtk.Label()
        self.label_gentab_gensearch.set_markup("<span font = \"Freestyle Script 55\" foreground=\"red\" >General Search</span>")
        self.Vbox_gensearch.pack_start(self.label_gentab_gensearch, False, False, 0)
        self.Vbox_gensearch.pack_start(self.Hbox_gensearch, False, False, 0)

        #--------------------General Search Ends Here---------------------#

        #--------------------HOF Search Starts Here-----------------------#
        self.label_constituency_Hof = Gtk.Label("Assembly Name", margin_start=0)
        self.label_name_hof = Gtk.Label("Head of Family Name", margin_start=0)
        self.label_voterid_hof = Gtk.Label("Voter ID Card No.", margin_start=0)
        self.entry_constituency_hof = Gtk.Entry(text="{}".format(ac_name), editable=False, margin_end=0)
        self.entry_name_hof = Gtk.Entry(max_length=20, xalign=0, margin_end=0)
        self.entry_voterid_hof = Gtk.Entry(margin_end=0)
        self.entry_name_hof.grab_focus_without_selecting()
        self.Button_Submit_hof = Gtk.Button("Submit")
        self.Button_Submit_hof.connect("clicked", self.show_search_results)

        self.grid_Hofsearch = Gtk.Grid(row_spacing=15, column_homogeneous=True, row_homogeneous=False)
        self.grid_Hofsearch.attach(self.label_constituency_Hof, 0, 0, 1, 1)
        self.grid_Hofsearch.attach(self.entry_constituency_hof, 2, 0, 1, 1)
        self.grid_Hofsearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 1, 3, 1)
        self.grid_Hofsearch.attach(self.label_name_hof, 0, 2, 1, 1)
        self.grid_Hofsearch.attach(self.entry_name_hof, 2, 2, 1, 1)
        self.grid_Hofsearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 3, 3, 1)
        self.grid_Hofsearch.attach(self.label_voterid_hof, 0, 4, 1, 1)
        self.grid_Hofsearch.attach(self.entry_voterid_hof, 2, 4, 1, 1)

        self.grid_Hofsearch.attach(self.Button_Submit_hof, 1, 5, 1, 1)
        self.grid_Hofsearch.set_border_width(20)

        self.Frame_Hofsearch = Gtk.Frame(vexpand=False)
        self.Frame_Hofsearch.set_hexpand(False)
        self.Frame_Hofsearch.set_hexpand_set(False)
        self.Frame_Hofsearch.add(self.grid_Hofsearch)
        self.Frame_Hofsearch.set_border_width(0)

        self.Hbox_Hofsearch = Gtk.Box(homogeneous=False)
        self.Hbox_Hofsearch.set_center_widget(self.Frame_Hofsearch)


        self.Vbox_Hofsearch = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL)
        self.label_hoftab_hofsearch = Gtk.Label()
        self.label_hoftab_hofsearch.set_markup(
            "<span font = \"Freestyle Script 50\" foreground=\"blue\" >Head Of Family Search</span>")
        self.Vbox_Hofsearch.pack_start(self.label_hoftab_hofsearch, False, False, 0)
        self.Vbox_Hofsearch.pack_start(self.Hbox_Hofsearch, False, False, 0)

        #------------------------HOF Search Ends Here----------------------#

        #------------------------Age wise starts Here----------------------$

        self.label_constituency_age = Gtk.Label("Assembly Name", margin_start=0)
        self.label_name_age = Gtk.Label("Voter's Name", margin_start=0)
        self.label_age_age = Gtk.Label("Age", margin_start=0)
        self.entry_constituency_age = Gtk.Entry(text="{}".format(ac_name), editable=False, margin_end=0)
        self.entry_name_age = Gtk.Entry(max_length=20, xalign=0, margin_end=0)
        self.entry_minage_age = Gtk.Entry(max_length=2, xalign=0, margin_end=0)
        self.entry_maxage_age = Gtk.Entry(max_length=2, xalign=0, margin_end=0)
        self.Hbox_min_max_age = Gtk.Box(homogeneous=True, spacing=10, hexpand=False)
        self.Hbox_min_max_age.pack_start(self.entry_minage_age, False, True, 0)
        self.entry_minage_age.set_max_width_chars(2)
        self.entry_minage_age.set_width_chars(2)
        self.Hbox_min_max_age.pack_start(Gtk.Label("TO"), False, True, 0)
        self.Hbox_min_max_age.pack_start(self.entry_maxage_age, False, True, 0)
        self.entry_maxage_age.set_width_chars(2)
        self.entry_maxage_age.set_max_width_chars(2)
        self.Button_Submit_age = Gtk.Button("Submit")
        self.Button_Submit_age.connect("clicked", self.show_search_results_age)
        for entry_age in [self.entry_name_age, self.entry_minage_age,self.entry_maxage_age]:
            entry_age.connect("activate", self.show_search_results_age)

        self.grid_agesearch = Gtk.Grid(row_spacing=15, column_homogeneous=True, row_homogeneous=False)
        self.grid_agesearch.attach(self.label_constituency_age, 0, 0, 1, 1)
        self.grid_agesearch.attach(self.entry_constituency_age, 2, 0, 1, 1)
        self.grid_agesearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 1, 3, 1)
        self.grid_agesearch.attach(self.label_name_age, 0, 2, 1, 1)
        self.grid_agesearch.attach(self.entry_name_age, 2, 2, 1, 1)
        self.grid_agesearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 3, 3, 1)
        self.grid_agesearch.attach(self.label_age_age, 0, 4, 1, 1)
        self.grid_agesearch.attach(self.Hbox_min_max_age, 2, 4, 1, 1)
        #self.grid_agesearch.attach(Gtk.Entry(), 2, 4, 1, 1)
        self.grid_agesearch.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                 margin_start=0), 0, 5, 3, 1)
        self.grid_agesearch.attach(self.Button_Submit_age, 1, 6, 1, 1)
        self.grid_agesearch.set_border_width(20)

        self.Frame_agesearch = Gtk.Frame(vexpand=False)
        self.Frame_agesearch.set_hexpand(False)
        self.Frame_agesearch.set_hexpand_set(False)
        self.Frame_agesearch.add(self.grid_agesearch)
        self.Frame_agesearch.set_border_width(0)

        self.Hbox_agesearch = Gtk.Box(homogeneous=False)
        self.Hbox_agesearch.set_center_widget(self.Frame_agesearch)

        self.Vbox_agesearch = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL)
        self.label_gentab_agesearch = Gtk.Label()
        self.label_gentab_agesearch.set_markup(
            "<span font = \"Freestyle Script 55\" foreground=\"#9B8C5C\" >Age Wise Search</span>")
        self.Vbox_agesearch.pack_start(self.label_gentab_agesearch, False, False, 0)
        self.Vbox_agesearch.pack_start(self.Hbox_agesearch, False, False, 0)



         #-----------------------Age wise ends here-----------------------#

        self.Vbox_stackswitcher_and_overlay = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)

        self.castewise_temp = Gtk.Label("")
        self.stack_middle.add_titled(self.Vbox_gensearch, "gen_search", "General")
        self.stack_middle.add_titled(self.Vbox_Hofsearch, "hof_search", "HOF")
        self.stack_middle.add_titled(self.castewise_temp, "castewise_search", "Caste Wise")
        self.stack_middle.add_titled(self.Vbox_agesearch, "agewise_search", "Age Wise")

        #self.Button_arrow_backtodash = Gtk.Button()
        #self.Button_arrow_backtodash.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        #self.Button_arrow_backtodash.connect("clicked", self.back_to_dashboard)
        self.Button_text_backtodash = Gtk.Button("Dashboard")
        self.Button_text_backtodash.connect("clicked", self.back_to_dashboard)

        self.hbox_stack_switcher_middle = Gtk.Box(homogeneous=False)
        self.stack_switcher_middle = Gtk.StackSwitcher()
        self.stack_switcher_middle.set_stack(self.stack_middle)
        self.hbox_stack_switcher_middle.set_center_widget(self.stack_switcher_middle)
        #self.hbox_stack_switcher_middle.pack_start(self.Button_arrow_backtodash, False, False, 0)
        self.hbox_stack_switcher_middle.pack_start(self.Button_text_backtodash, False, False, 0)

        #----------------------------Dashboard----------------------------#
        self.Overlay_dashboard = Gtk.Overlay()

        self.Vbox_stackswitcher_and_overlay.pack_start(self.hbox_stack_switcher_middle, False, False, 20)
        self.Vbox_stackswitcher_and_overlay.pack_start(self.Overlay_dashboard, True, True, 0)

        self.Hbox_Lower.pack_start(self.root_stack, True, True, 0)


        self.Hbox_button_back_for_overlay = Gtk.Box(homogeneous=False)
        self.Button_back_for_overlay = Gtk.Button(valign=Gtk.Align.CENTER, hexpand=False)
        self.Button_back_for_overlay.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.Button_back_for_overlay.connect("clicked", self.reveal_hide_stackbar)
        self.Hbox_button_back_for_overlay.pack_start(self.Button_back_for_overlay, False, False, 0)
        self.Overlay_dashboard.add(self.stack_middle)
        self.Overlay_dashboard.add_overlay(self.Hbox_button_back_for_overlay)
        self.Overlay_dashboard.set_overlay_pass_through(self.Hbox_button_back_for_overlay, True)
        #self.Overlay_dashboard.add_overlay(self.Button_back_for_overlay)


        self.Frame = Gtk.Frame()
        self.box_middleRootframe.pack_start(self.Frame, True, True, 0)
        self.Frame.set_border_width(0)
        self.label_frame = Gtk.Label()
        self.label_frame.set_markup("<span font = \"Monotype Corsiva Italic 20\" foreground=\"red\" >Select an option "
                                    "below</span>")
        self.Frame.set_label_widget(self.label_frame)
        self.Frame.set_shadow_type(Gtk.ShadowType.OUT)
        self.Frame.set_label_align(0.5,0.5)
        self.scrollwindow_frame = Gtk.ScrolledWindow()
        self.Frame.add(self.scrollwindow_frame)
        self.Vbox_scrollwindow = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous = False)
        self.scrollwindow_frame.add(self.Vbox_scrollwindow)

        #--------------------Search Frame Starts Here---------------------#
        self.Frame_search = Gtk.Frame()
        self.Frame_search.set_border_width(10)
        self.label_Frame_search = Gtk.Label()
        self.label_Frame_search.set_markup("<span font = \"Calibri Italic 12\" foreground=\"green\" >Search</span>")
        self.Frame_search.set_label_widget(self.label_Frame_search)
        self.Frame_search.set_shadow_type(Gtk.ShadowType.OUT)
        self.Frame_search.set_label_align(0.03, 0.5)
        self.Vbox_scrollwindow.pack_start(self.Frame_search, False, False, 5)

        self.Vbox_frame_search = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous = False)
        self.Frame_search.add(self.Vbox_frame_search)

        self.Hbox1_frame_search = Gtk.Box(spacing=6, homogeneous=True)
        self.Hbox1_frame_search.set_border_width(10)
        self.Vbox_frame_search.pack_start(self.Hbox1_frame_search, True, True, 0)

        self.Button_generalsearch = Gtk.Button("General Search")
        self.image_generalsearchbtn = Gtk.Image()
        self.image_generalsearchbtn.set_from_file('GenSearch.png')
        self.Button_generalsearch.set_always_show_image(True)
        self.Button_generalsearch.set_image(self.image_generalsearchbtn)
        self.Button_generalsearch.set_image_position(Gtk.PositionType.TOP)
        self.Button_generalsearch.connect("clicked", self.switch_to_selected_search)
        self.Hbox1_frame_search.pack_start(self.Button_generalsearch, True, False, 0)

        self.Button_HOFsearch = Gtk.Button.new_with_mnemonic("_Head of Family")
        self.image_hofsearchbtn = Gtk.Image()
        self.image_hofsearchbtn.set_from_file(
            'Hof.png')
        self.Button_HOFsearch.set_always_show_image(True)
        self.Button_HOFsearch.set_image(self.image_hofsearchbtn)
        self.Button_HOFsearch.set_image_position(Gtk.PositionType.TOP)
        self.Button_HOFsearch.connect("clicked", self.switch_to_selected_search)
        self.Hbox1_frame_search.pack_start(self.Button_HOFsearch, True, False, 5)

        self.Button_castesearch = Gtk.Button.new_with_mnemonic("_Caste Wise Search")
        self.image_castesearchbtn = Gtk.Image()
        self.image_castesearchbtn.set_from_file(
            'CasteSearch.png')
        self.Button_castesearch.set_always_show_image(True)
        self.Button_castesearch.set_image(self.image_castesearchbtn)
        self.Button_castesearch.set_image_position(Gtk.PositionType.TOP)
        #self.Button_castesearch.connect("clicked", self.switch_to_selected_search)
        self.Hbox1_frame_search.pack_start(self.Button_castesearch, True, False, 0)

        self.Hbox2_frame_search = Gtk.Box(spacing=6, homogeneous=True)
        self.Hbox2_frame_search.set_border_width(10)
        self.Vbox_frame_search.pack_start(self.Hbox2_frame_search, True, True, 0)

        self.Button_agewisesearch = Gtk.Button("Age Wise Search")
        self.image_placeholder = Gtk.Image()
        self.image_placeholder.set_from_file(
            'AgeSearch.png')
        self.Button_agewisesearch.set_always_show_image(True)
        self.Button_agewisesearch.set_image(self.image_placeholder)
        self.Button_agewisesearch.set_image_position(Gtk.PositionType.TOP)
        self.Button_agewisesearch.connect("clicked", self.switch_to_selected_search)
        self.Hbox2_frame_search.pack_start(self.Button_agewisesearch, True, False, 0)



        # --------------------Search Frame Ends Here---------------------#

        # --------------------Placeholder Frame Starts Here---------------------#

        self.Frame_Extras = Gtk.Frame()
        self.Frame_Extras.set_border_width(10)
        self.label_Frame_Extras = Gtk.Label()
        self.label_Frame_Extras.set_markup("<span font = \"Calibri Italic 12\" foreground=\"green\" >Extras</span>")
        self.Frame_Extras.set_label_widget(self.label_Frame_Extras)
        self.Frame_Extras.set_shadow_type(Gtk.ShadowType.OUT)
        self.Frame_Extras.set_label_align(0.03, 0.5)
        self.Vbox_scrollwindow.pack_start(self.Frame_Extras, False, False, 5)

        self.Vbox_frame_Placeholder = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.Frame_Extras.add(self.Vbox_frame_Placeholder)

        self.Hbox3_frame_Placeholder = Gtk.Box(spacing=6, homogeneous=True)
        self.Hbox3_frame_Placeholder.set_border_width(10)
        self.Vbox_frame_Placeholder.pack_start(self.Hbox3_frame_Placeholder, True, True, 0)

        self.Button_Duplicate_finder = Gtk.Button("Duplicate Finder")
        self.image_duplicate = Gtk.Image()
        self.image_duplicate.set_from_file(
            'duplicate.png')
        self.Button_Duplicate_finder.set_always_show_image(True)
        self.Button_Duplicate_finder.set_image(self.image_duplicate)
        self.Button_Duplicate_finder.set_image_position(Gtk.PositionType.TOP)
        self.Button_Duplicate_finder.connect("clicked", self.switch_to_selected_search)
        self.Hbox3_frame_Placeholder.pack_start(self.Button_Duplicate_finder, True, False, 0)

        self.Button_voter_slip = Gtk.Button("Voter Slip Generator")
        self.image_voter_slip = Gtk.Image()
        self.image_voter_slip.set_from_file(
            'voter slip.png')
        self.Button_voter_slip.set_always_show_image(True)
        self.Button_voter_slip.set_image(self.image_voter_slip)
        self.Button_voter_slip.set_image_position(Gtk.PositionType.TOP)
        self.Button_voter_slip.connect("clicked", self.switch_to_selected_search)
        self.Hbox3_frame_Placeholder.pack_start(self.Button_voter_slip, True, False, 0)



        # --------------------Placeholder Frame Ends Here---------------------#

        # --------------------Contsct Frame Starts Here---------------------#

        self.Frame_contact_us = Gtk.Frame()
        self.Frame_contact_us.set_border_width(10)
        self.label_Frame_contact_us = Gtk.Label()
        self.label_Frame_contact_us.set_markup("<span font = \"Calibri Italic 12\" foreground=\"green\" >Contact Us</span>")
        self.Frame_contact_us.set_label_widget(self.label_Frame_contact_us)
        self.Frame_contact_us.set_shadow_type(Gtk.ShadowType.OUT)
        self.Frame_contact_us.set_label_align(0.03, 0.5)
        self.Vbox_scrollwindow.pack_start(self.Frame_contact_us, False, False, 5)

        self.Vbox_frame_contact_us = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.Frame_contact_us.add(self.Vbox_frame_contact_us)

        self.Hbox3_frame_contact_us = Gtk.Box(spacing=6, homogeneous=True)
        self.Hbox3_frame_contact_us.set_border_width(10)
        self.Vbox_frame_contact_us.pack_start(self.Hbox3_frame_contact_us, True, True, 0)

        self.Button_contact_us = Gtk.Button("Contact Us")
        self.image_contact_us = Gtk.Image()
        self.image_contact_us.set_from_file(
            'contact_us.png')
        self.Button_contact_us.set_always_show_image(True)
        self.Button_contact_us.set_image(self.image_contact_us)
        self.Button_contact_us.set_image_position(Gtk.PositionType.TOP)
        self.Button_contact_us.connect("clicked", self.switch_to_selected_search)
        self.Hbox3_frame_contact_us.pack_start(self.Button_contact_us, True, False, 0)

        #---------------------Dashboard Ends Here------------------------_#
        # --------------------Lower Frame Ends Here---------------------#

        #self.RootVbox.pack_start(self.hbox_stack_switcher_middle, False, False, 20)
        #self.RootVbox.pack_start(self.Overlay_dashboard, True, True, 0)

        #----------------------Extras Statrs Here------------------------------#

        self.Vbox_extras = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        #-------------------------Duplicate finder starts here-----------------#
        self.label_constituency_dfinder = Gtk.Label("Assembly Name", margin_start=0)
        self.label_name_dfinder = Gtk.Label("Voter's Name", margin_start=0)
        self.label_rlnname_dfinder = Gtk.Label("Relation's Name", margin_start=0)
        self.label_voterid_dfinder = Gtk.Label("Voter ID Card No.", margin_start=0)
        self.entry_constituency_dfinder = Gtk.Entry(text="{}".format(ac_name), editable=False, margin_end=0)
        self.entry_name_dfinder = Gtk.Entry(max_length=20, xalign=0, margin_end=0, can_focus=True)
        self.entry_rlnname_dfinder = Gtk.Entry(margin_end=0)
        self.entry_voterid_dfinder = Gtk.Entry(margin_end=0)
        self.entry_name_dfinder.connect("activate", self.grab_focus_on_name)
        self.Button_Submit_dfinder = Gtk.Button("Submit")
        self.Button_Submit_dfinder.set_name("btn_submit")
        self.Button_Submit_dfinder.connect("clicked", self.show_search_results_gen)
        self.grid_DuplicateFinder = Gtk.Grid(row_spacing=15, column_homogeneous=True, row_homogeneous=False)
        self.grid_DuplicateFinder.attach(self.label_constituency_dfinder, 0, 0, 1, 1)
        self.grid_DuplicateFinder.attach(self.entry_constituency_dfinder, 2, 0, 1, 1)
        self.grid_DuplicateFinder.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                       margin_start=0), 0, 1, 3, 1)
        self.grid_DuplicateFinder.attach(self.label_name_dfinder, 0, 2, 1, 1)
        self.grid_DuplicateFinder.attach(self.entry_name_dfinder, 2, 2, 1, 1)
        self.grid_DuplicateFinder.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                       margin_start=0), 0, 3, 3, 1)
        self.grid_DuplicateFinder.attach(self.label_rlnname_dfinder, 0, 4, 1, 1)
        self.grid_DuplicateFinder.attach(self.entry_rlnname_dfinder, 2, 4, 1, 1)
        self.grid_DuplicateFinder.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                                       margin_start=0), 0, 5, 3, 1)
        self.grid_DuplicateFinder.attach(self.label_voterid_dfinder, 0, 6, 1, 1)
        self.grid_DuplicateFinder.attach(self.entry_voterid_dfinder, 2, 6, 1, 1)

        self.grid_DuplicateFinder.attach(self.Button_Submit_dfinder, 1, 7, 1, 1)
        self.grid_DuplicateFinder.set_border_width(20)

        self.Frame_DuplicateFinder = Gtk.Frame(vexpand=False)
        self.Frame_DuplicateFinder.set_hexpand(False)
        self.Frame_DuplicateFinder.set_hexpand_set(False)
        self.Frame_DuplicateFinder.add(self.grid_DuplicateFinder)
        self.Frame_DuplicateFinder.set_border_width(0)


        self.Hbox_DuplicateFinder = Gtk.Box(homogeneous=False)
        self.Hbox_DuplicateFinder.set_center_widget(self.Frame_DuplicateFinder)

        self.Vbox_DuplicateFinder = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL)
        self.label_gentab_DuplicateFinder = Gtk.Label()
        self.label_gentab_DuplicateFinder.set_markup(
            "<span font = \"Freestyle Script 55\" foreground=\"violet\" >Duplicate Finder</span>")
        self.Vbox_DuplicateFinder.pack_start(self.label_gentab_DuplicateFinder, False, False, 0)
        self.Vbox_DuplicateFinder.pack_start(self.Hbox_DuplicateFinder, False, False, 0)

        #-------------------------------Duplicate Finder Ends Here----------------------------#

        #---------------------------Voter Slip Generator Starts Here--------------------------#
        self.label_constituency_vslip = Gtk.Label("Assembly Name", margin_start=0)
        self.label_voterid_vslip = Gtk.Label("Voter ID Card No.", margin_start=0)
        self.entry_constituency_vslip = Gtk.Entry(text="{}".format(ac_name), editable=False, margin_end=0)
        self.entry_voterid_vslip = Gtk.Entry(margin_end=0)
        self.Button_Submit_vslip = Gtk.Button("Submit")
        self.Button_Submit_vslip.connect("clicked", self.pass_voter_id_for_vlist)

        self.grid_vslip = Gtk.Grid(row_spacing=15, column_homogeneous=True, row_homogeneous=False)
        self.grid_vslip.attach(self.label_constituency_vslip, 0, 0, 1, 1)
        self.grid_vslip.attach(self.entry_constituency_vslip, 2, 0, 1, 1)
        self.grid_vslip.attach(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_end=0,
                                             margin_start=0), 0, 1, 3, 1)
        self.grid_vslip.attach(self.label_voterid_vslip, 0, 2, 1, 1)
        self.grid_vslip.attach(self.entry_voterid_vslip, 2, 2, 1, 1)

        self.grid_vslip.attach(self.Button_Submit_vslip, 1, 3, 1, 1)
        self.grid_vslip.set_border_width(20)

        self.Frame_vslip = Gtk.Frame(vexpand=False)
        self.Frame_vslip.set_hexpand(False)
        self.Frame_vslip.set_hexpand_set(False)
        self.Frame_vslip.add(self.grid_vslip)
        self.Frame_vslip.set_border_width(0)

        self.Hbox_vslip = Gtk.Box(homogeneous=False)
        self.Hbox_vslip.set_center_widget(self.Frame_vslip)

        self.Vbox_vslip = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL)
        self.label_vsliptab_vslipsearch = Gtk.Label()
        self.label_vsliptab_vslipsearch.set_markup(
            "<span font = \"Freestyle Script 50\" foreground=\"blue\" >Voter Slip Generator</span>")
        self.Vbox_vslip.pack_start(self.label_vsliptab_vslipsearch, False, False, 0)
        self.Vbox_vslip.pack_start(self.Hbox_vslip, False, False, 0)
        #---------------------------Voter Slip Generator Ends Here----------------------------#

        self.extras_stack = Gtk.Stack(homogeneous=False, interpolate_size=False)
        self.extras_stack.set_transition_type(14)
        self.extras_stack.set_transition_duration(1000)
        self.extras_stack.add_titled(self.Vbox_DuplicateFinder, "duplicate", "Duplicate Finder")
        self.extras_stack.add_titled(self.Vbox_vslip, "voter slip", "Voter Slip Generator")
        self.extras_stack_switcher = Gtk.StackSwitcher()
        self.extras_stack_switcher.set_margin_top(15)
        self.extras_stack_switcher.set_stack(self.extras_stack)

        self.Overlay_Extras = Gtk.Overlay()
        self.Overlay_Extras.add(self.extras_stack)

        self.Hbox_extras_stack_switcher = Gtk.Box(homogeneous=False)
        self.Hbox_extras_stack_switcher.set_center_widget(self.extras_stack_switcher)

        self.Vbox_extras.pack_start(self.Hbox_extras_stack_switcher, False, False, 0)
        self.Vbox_extras.pack_start(self.Overlay_Extras, False, False, 0)

        self.Hbox_button_back_for_overlay_extras = Gtk.Box(homogeneous=False)

        self.Overlay_Extras.add_overlay(self.Hbox_button_back_for_overlay_extras)
        self.Overlay_Extras.set_overlay_pass_through(self.Hbox_button_back_for_overlay_extras, True)

        self.Button_back_for_overlay_extras = Gtk.Button(valign=Gtk.Align.CENTER, hexpand=False)
        self.Button_back_for_overlay_extras.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.Button_back_for_overlay_extras.connect("clicked", self.reveal_hide_stackbar)

        self.Hbox_button_back_for_overlay_extras.pack_start(self.Button_back_for_overlay_extras, False, False, 0)

        #------------------------Extras Ends Here---------------------#

        #-----------------------Android Statrs Here-------------------#

        self.Overlay_android = Gtk.Overlay()

        self.Vbox_android = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL, spacing=25)
        self.Overlay_android.add(self.Vbox_android)

        self.Hbox_button_back_for_overlay_android = Gtk.Box(homogeneous=False)

        self.Button_back_for_overlay_android = Gtk.Button(valign=Gtk.Align.CENTER, hexpand=False)
        self.Button_back_for_overlay_android.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.Button_back_for_overlay_android.connect("clicked", self.reveal_hide_stackbar)
        self.Hbox_button_back_for_overlay_android.pack_start(self.Button_back_for_overlay_android, False, False, 0)

        self.Overlay_android.add_overlay(self.Hbox_button_back_for_overlay_android)
        self.Overlay_android.set_overlay_pass_through(self.Hbox_button_back_for_overlay_android, True)

        self.label_android_coming_soon = Gtk.Label()
        self.label_android_coming_soon.set_margin_top(15)
        self.label_android_coming_soon.set_markup(
            "<span font = \"Matura MT Script Capitals 45\" foreground=\"tomato\" >Android App Coming Soon</span>")

        self.image_android = Gtk.Image()
        self.image_android.set_from_file('android.png')

        self.Vbox_android.pack_start(self.label_android_coming_soon, False, False, 0)
        self.Vbox_android.pack_start(self.image_android, False, False, 0)


        #-----------------------Android Ends Here---------------------#

        #-----------------------Contact Us Starts Here---------------------#

        self.Overlay_contact_us = Gtk.Overlay()

        self.Vbox_contact_us = Gtk.Box(homogeneous=False, orientation=Gtk.Orientation.VERTICAL, spacing=6, can_focus=False)
        self.Overlay_contact_us.add(self.Vbox_contact_us)

        self.Hbox_button_back_for_overlay_contact_us = Gtk.Box(homogeneous=False)

        self.Button_back_for_overlay_contact_us = Gtk.Button(valign=Gtk.Align.CENTER, hexpand=False)
        self.Button_back_for_overlay_contact_us.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.Button_back_for_overlay_contact_us.connect("clicked", self.reveal_hide_stackbar)
        self.Hbox_button_back_for_overlay_contact_us.pack_start(self.Button_back_for_overlay_contact_us, False, False,
                                                                0)
        self.Overlay_contact_us.add_overlay(self.Hbox_button_back_for_overlay_contact_us)
        self.Overlay_contact_us.set_overlay_pass_through(self.Hbox_button_back_for_overlay_contact_us, True)

        self.label_bd_sharma = Gtk.Label("Brahmdev Sharma", margin_start=0)
        self.label_phone = Gtk.Label("Contact Number : 9868505151 , 9136181685", margin_start=0)
        self.label_email = Gtk.Label("Email Id : brahmdev2000@gmail.com", margin_start=0)
        self.label_fax = Gtk.Label("Fax: N/A" ,margin_start=0)

        self.label_get_in_touch = Gtk.Label()
        self.label_get_in_touch.connect("show", self.grab_focus_on_label_touch)
        self.label_get_in_touch.set_markup(
            "<span font = \"Calibri 25\" foreground=\"Green\">Get in Touch </span>")
        self.label_please_fill_out = Gtk.Label("Please fill out the quick form and we will be in touch with "
                                               "lightening speed")
        self.entry_name_contact_us = Gtk.Entry()
        self.entry_name_contact_us.set_placeholder_text("Name")
        self.entry_email_contact_us = Gtk.Entry()
        self.entry_email_contact_us.set_placeholder_text("Email")
        self.entry_message_contact_us = Gtk.Entry()
        self.entry_message_contact_us.set_placeholder_text("Message")

        self.Button_Submit_contact = Gtk.Button("Submit")
        self.Button_Submit_contact.set_name("btn_submit_contact")
        self.Hbox_submitBtn_contact_us = Gtk.Box(homogeneous=False)
        self.Hbox_submitBtn_contact_us.set_center_widget(self.Button_Submit_contact)

        self.grid_contact_us = Gtk.Grid(row_spacing=15, column_spacing=15, column_homogeneous=False, row_homogeneous=True)
        self.grid_contact_us.attach(self.label_bd_sharma, 0, 0, 1, 1)
        self.grid_contact_us.attach(self.label_phone ,0, 1, 1, 1)
        self.grid_contact_us.attach(self.label_email, 0, 2, 1, 1)
        self.grid_contact_us.attach(self.label_fax, 0, 3, 1, 1)

        self.grid_contact_us.attach(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL, margin_end=0,
                                                       margin_start=0), 1, 0, 1, 7)

        self.grid_contact_us.attach(self.label_get_in_touch, 2, 0, 1, 1)
        self.grid_contact_us.attach(self.label_please_fill_out, 2, 1, 1, 1)
        self.grid_contact_us.attach(self.entry_name_contact_us, 2, 2, 1, 1)
        self.grid_contact_us.attach(self.entry_email_contact_us, 2, 3, 1, 1)
        self.grid_contact_us.attach(self.entry_message_contact_us, 2, 4, 1, 1)
        self.grid_contact_us.attach(self.Hbox_submitBtn_contact_us, 2, 5, 1, 1)

        self.grid_contact_us.set_border_width(20)

        self.Frame_contact_us = Gtk.Frame(vexpand=False, margin_start=20)
        self.Frame_contact_us.set_hexpand(False)
        self.Frame_contact_us.set_hexpand_set(False)
        self.Frame_contact_us.add(self.grid_contact_us)
        self.Frame_contact_us.set_border_width(0)

        self.Hbox_contact_us = Gtk.Box(homogeneous=True)
        self.Hbox_contact_us.pack_start(self.Frame_contact_us, True, True, 0)

        self.label_contact_us = Gtk.Label()
        self.label_contact_us.set_markup(
            "<span font = \"Georgia 55\" foreground=\"brown\" >Contact Us </span>")
        self.Vbox_contact_us.pack_start(self.label_contact_us, False, False, 0)

        self.Vbox_contact_us.pack_start(self.Hbox_contact_us, False, False, 0)


        #-----------------------Contact Us Ends Here---------------------#

        self.root_stack.add_titled(self.Vbox_stackswitcher_and_overlay, "Dashboard", "Dashboard")
        self.root_stack.add_titled(self.Vbox_extras, "Extras", "Extras")
        self.root_stack.add_titled(self.Overlay_android, "Android", "Android App")
        self.root_stack.add_titled(self.Overlay_contact_us, "Contact", "Contact Us")

        self.RootVbox.pack_start(self.Hbox_Lower, True, True, 0)



    def open_popover(self, button):
        # Toggle
        if self.popover_menu.get_visible():
            self.popover_menu.hide()
        else:
            self.popover_menu.show_all()

    def clear_frame(self, button):
        list_of_children = self.RootVbox.get_children()
        print(list_of_children)
        if self.stack_middle in list_of_children :
            self.RootVbox.remove(self.stack_middle)

    def hide_stack_switcher(self, button):
        self.current_middle_tab = self.stack_middle.get_visible_child_name()
        if self.current_middle_tab == "Dashboard":
            self.hbox_stack_switcher_middle.hide()

    def switch_to_selected_search(self, button):

        if button == self.Button_generalsearch:
            self.stack_middle.set_visible_child_name("gen_search")
        elif button == self.Button_HOFsearch:
            self.stack_middle.set_visible_child_name("hof_search")
        elif button == self.Button_castesearch:
            self.stack_middle.set_visible_child_name("castewise_search")
        elif button == self.Button_agewisesearch:
            self.stack_middle.set_visible_child_name("agewise_search")
        elif button == self.Button_Duplicate_finder:
            self.extras_stack.set_visible_child_name("duplicate")
            self.root_stack.set_visible_child_name("Extras")
        elif button == self.Button_voter_slip:
            self.extras_stack.set_visible_child_name("voter slip")
            self.root_stack.set_visible_child_name("Extras")
        elif button == self.Button_contact_us:
            self.root_stack.set_visible_child_name("Contact")

        self.current_middle_tab = self.stack_middle.get_visible_child_name()
        if self.current_middle_tab != "Dashboard":
            self.hbox_stack_switcher_middle.show()

    def back_to_dashboard(self, button):
        self.stack_middle.set_visible_child_name("Dashboard")
        self.hide_stack_switcher(button)

    def show_search_results_gen(self, button):
        self.name = self.entry_name.get_text().strip()
        self.rlnname = self.entry_rlnname.get_text().strip()
        self.voteridcard = self.entry_voterid.get_text().strip().upper()
        self.clear_entries_gen()
        self.append_and_show_result_list_gen(self.name, self.rlnname, self.voteridcard)

    def append_and_show_result_list_gen(self, name, rlnname, voteridcard):
        self.conn = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.cur = self.conn.cursor()
        if name != "" and rlnname == "" and voteridcard == "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE FM_NAME_V LIKE ?", (name + '%',))

        elif name != "" and rlnname == "" and voteridcard != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE FM_NAME_V LIKE ? AND IDCARD_NO=?", (name + '%', voteridcard))

        elif name != "" and rlnname != "" and voteridcard == "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE FM_NAME_V LIKE ? AND RLN_FM_NAME_V LIKE ?",
                        (name + '%', rlnname + '%'))

        elif name != "" and rlnname != "" and voteridcard != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE FM_NAME_V LIKE ? AND RLN_FM_NAME_V LIKE ? AND IDCARD_NO=?",
                        (name + '%',
                         rlnname + '%',
                         voteridcard))
        elif name == "" and rlnname == "" and voteridcard != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE IDCARD_NO=?", (voteridcard,))

        self.result = self.cur.fetchall()
        if self.result != []:
            self.win2 = TreeViewFilterWindow()
            self.cur.close()

        else:
            self.dialog_no_records_found("Gen")


    def append_and_show_result_list_hof(self, name, voteridcard):
        self.conn = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.cur = self.conn.cursor()
        if name != "" and voteridcard == "":
            self.cur.execute("SELECT * FROM HOF WHERE FM_NAME_V LIKE ?", (name + '%',))

        elif name != "" and voteridcard != "":
            self.cur.execute("SELECT * FROM HOF WHERE FM_NAME_V LIKE ? AND IDCARD_NO=?", (name + '%', voteridcard))

        elif name == "" and voteridcard != "":
            self.cur.execute("SELECT * FROM HOF WHERE IDCARD_NO=?", (voteridcard,))

        self.result = self.cur.fetchall()
        if self.result != []:
            win2 = HofWindow()
            self.cur.close()

        else:
            self.dialog_no_records_found("Hof")

    def append_and_show_result_list_age(self, name, minage, maxage):
        self.conn = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.cur = self.conn.cursor()
        if name != "" and minage != "" and maxage != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE FM_NAME_V LIKE ? AND Age BETWEEN ? AND ? ", (name + '%', minage, maxage))

        elif name == "" and minage != "" and maxage != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE Age BETWEEN ? AND ? ", (minage, maxage))

        self.result = self.cur.fetchall()
        if self.result != []:
            win2 = TreeViewFilterWindow()
            self.cur.close()

        else:
            self.dialog_no_records_found("age")

    def show_voter_list(self, voteridcard):
        self.conn = sqlite3.connect('C:\Windows\System32\\fxwin32.db')
        self.cur = self.conn.cursor()
        if voteridcard != "":
            self.cur.execute("SELECT * FROM ELEWARD WHERE IDCARD_NO=?", (voteridcard,))

        self.result = self.cur.fetchall()
        if self.result != []:
           self.win2 = VoterList()
           self.cur.close()

        else:
           self.dialog_no_records_found("vlist")


    def show_search_results(self, button):
        self.name = self.entry_name_hof.get_text().strip()
        self.voteridcard = self.entry_voterid_hof.get_text().strip().upper()
        self.clear_entries_hof()
        self.append_and_show_result_list_hof(self.name, self.voteridcard)

    def show_search_results_gen_enter(self, button, ev, data=None):
        if ev.keyval == 65076:
            self.show_search_results_gen(button)

    def show_search_results_age(self, button):
        self.name = self.entry_name_age.get_text().strip()
        self.minage = self.entry_minage_age.get_text().strip()
        self.maxage = self.entry_maxage_age.get_text().strip()
        self.clear_entries_age()
        self.append_and_show_result_list_age(self.name, self.minage, self.maxage)

    def pass_voter_id_for_vlist(self, button):
        self.vidcard = self.entry_voterid_vslip.get_text().strip().upper()
        self.entry_voterid_vslip.set_text("")
        self.show_voter_list(self.vidcard)

    def dialog_no_records_found(self, tab):
        dialog = Gtk.MessageDialog(self, 1, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "NO RECORDS FOUND !")
        dialog.format_secondary_text("Please double check your entries and try again ")
        dialog.run()
        if tab == "Gen":
            self.clear_entries_gen()
        elif tab == "Hof":
            self.clear_entries_hof()
        elif tab == "age":
            self.clear_entries_age()
        elif tab == "vlist":
            self.entry_voterid_vslip.set_text("")

        dialog.destroy()

    def clear_entries_gen(self):
        self.entry_name.set_text("")
        self.entry_rlnname.set_text("")
        self.entry_voterid.set_text("")

    def clear_entries_hof(self):
        self.entry_name_hof.set_text("")
        self.entry_voterid_hof.set_text("")

    def clear_entries_age(self):
        self.entry_name_age.set_text("")
        self.entry_minage_age.set_text("")
        self.entry_maxage_age.set_text("")

    def reveal_hide_stackbar(self, button):
        reveal = self.Revealer_stackbar.get_reveal_child()
        self.Revealer_stackbar.set_reveal_child(not reveal)


    def grab_focus_on_name(self, entry):
        self.Button_Submit.grab_focus()

    def grab_focus_on_label_touch(self, widget):
        widget.grab_focus()

def hash(s):
    s = bytearray(s.encode("utf-8"))
    import hashlib
    m = hashlib.sha256(s)
    return m.hexdigest()

import os.path
if os.path.isfile("C:\Windows\System32\kwin64.dll"):
    file = open("C:\Windows\System32\kwin64.dll", "r")
    a = file.readline()
    from uuid import getnode as getMac
    import win32api
    mac = getMac()
    if hash(str(getMac()) + a + str(win32api.GetVolumeInformation("C:\\")[1] +
                                    win32api.GetVolumeInformation("C:\\")[2] +
                                    win32api.GetVolumeInformation("C:\\")[3]) + "B|)$*123")[0:4] == "0000":
        win = MainWindow()
        Style_Provider = Gtk.CssProvider()
        Style_Provider.load_from_path("FileStyle.css")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), Style_Provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()
    else:
        print("Wrong key")

else:
    print("No Key")

