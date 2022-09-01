import Tkinter

from MultiExplorer.src.GUI.Styles import DefaultStyle


class NavigateButton(Tkinter.Button, object):
    def __init__(self, to_screen_class_name, screen, master=None, cnf={}, **kw):
        super(NavigateButton, self).__init__(master, cnf, **kw)

        self.to_screen_class_name = to_screen_class_name

        self.screen = screen

        self.configure(
            command=lambda: self.navigate(),
            activebackground=DefaultStyle.button_active_bg_color,
            borderwidth="2",
        )

    def navigate(self):
        self.screen.navigate_by_class_name(self.to_screen_class_name)
