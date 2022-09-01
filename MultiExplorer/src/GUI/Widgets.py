import Tkinter

from MultiExplorer.src.GUI.Styles import DefaultStyle


class ScreenTitle(Tkinter.Label, object):
    def __init__(self, title, master=None, cnf={}, **kw):
        super(ScreenTitle, self).__init__(master, cnf, **kw)

        self.place(relx=0.5, anchor="n", height=50, relwidth=1)
        self.configure(activebackground=DefaultStyle.bg_color)
        self.configure(text=title)
