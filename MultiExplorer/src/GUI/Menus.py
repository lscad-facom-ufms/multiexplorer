import Tkinter as Tk

from MultiExplorer.src.GUI.Styles import DefaultStyle


class DefaultMenu(Tk.Menu, object):
    def __init__(self, master=None):
        super(DefaultMenu, self).__init__(
            master=master,
            font=DefaultStyle.font,
            bg=DefaultStyle.bg_color,
            fg=DefaultStyle.fg_color
        )

        master.configure(menu=self)

        self.settings_sub_menu = Tk.Menu(master, tearoff=0)

        self.add_cascade(menu=self.settings_sub_menu, label="Menu")

        self.settings_sub_menu.add_command(label="Settings")

        self.settings_sub_menu.add_command(label="Import")

        self.tools_sub_menu = Tk.Menu(master,tearoff=0)

        self.add_cascade(menu=self.tools_sub_menu,label="Tools")
