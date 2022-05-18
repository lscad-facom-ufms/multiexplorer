import Tkinter
import ttk

from Tkconstants import CENTER
from MultiExplorer.src.GUI.Menus import DefaultMenu
from MultiExplorer.src.GUI.Styles import DefaultStyle, DefaultStyleSettings


class MainWindow(Tkinter.Tk, object):
    frames = {}

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super(MainWindow, self).__init__(screenName, baseName, className, useTk, sync, use)

        self.geometry("1024x768")
        self.minsize(640, 480)
        self.maxsize(1920, 1080)
        self.resizable(1, 1)
        self.title("MultiExplorer")
        self.configure(highlightcolor="black")

        self.style = DefaultStyle()

        self.menu = DefaultMenu(self)

        self.frames = {
            LoadScreen.key: LoadScreen(self),
            LaunchScreen.key: LaunchScreen(self, focus=True),
            InputScreen.key: InputScreen(self),
        }

    def navigate(self, from_key, to_key):
        self.frames[from_key].pack_forget()

        self.frames[LoadScreen.key].pack(fill="both", expand=True)

        self.frames[from_key].close_gracefully()

        self.frames[to_key].prepare()

        self.frames[LoadScreen.key].pack_forget()

        self.frames[to_key].pack(fill="both", expand=True)


class ScreenFrame(Tkinter.Frame, object):
    key = 'abstract_screen'

    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(ScreenFrame, self).__init__(master, cnf, **kw)

        self.pack(fill="both", expand=True)

        if focus is True:
            self.tkraise()

    def navigate(self, to_key):
        self.master.navigate(self.key, to_key)

    def prepare(self):
        pass

    def close_gracefully(self):
        pass


class LoadScreen(ScreenFrame):
    key = 'load_screen'

    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(LoadScreen, self).__init__(master, cnf, focus, **kw)


class LaunchScreen(ScreenFrame):
    key = 'launch_screen'

    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(LaunchScreen, self).__init__(master, cnf, focus, **kw)

        self.me_logo_image = Tkinter.Label(self)
        self.me_logo_image.place(relx=0.5, anchor="n", height=150, width=250)
        self.me_logo_image.configure(activebackground=DefaultStyleSettings.bg_color)
        self.me_logo_image.configure(text='''MultiExplorer.png''')

        self.execution_flow_label_frame = Tkinter.LabelFrame(self)
        self.execution_flow_label_frame.place(relx=0.5, rely=0.5, anchor=CENTER, height=120, width=600)
        self.execution_flow_label_frame.configure(relief='groove')
        self.execution_flow_label_frame.configure(labelanchor='n')
        self.execution_flow_label_frame.configure(text='''Execution Flow''')

        self.execute_button = Tkinter.Button(
            self.execution_flow_label_frame,
            command=lambda: self.navigate(InputScreen.key)
        )
        self.execute_button.place(
            relx=0.6,
            rely=0.4,
            height=30,
            width=60,
            bordermode='ignore'
        )
        self.execute_button.configure(activebackground="#f9f9f9")
        self.execute_button.configure(borderwidth="2")
        self.execute_button.configure(text='''Run''')

        self.select_execution_flow_combobox = ttk.Combobox(self.execution_flow_label_frame)
        self.select_execution_flow_combobox.place(
            relx=0.177,
            rely=0.405,
            relheight=0.405,
            relwidth=0.392,
            bordermode='ignore'
        )
        self.value_list = ['Gpu', 'Cpu', 'Outros', ]
        self.select_execution_flow_combobox.configure(values=self.value_list)
        self.select_execution_flow_combobox.configure(textvariable=Tkinter.StringVar())
        self.select_execution_flow_combobox.configure(takefocus="")


class InputScreen(ScreenFrame):
    key = 'input_screen'

    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(InputScreen, self).__init__(master, cnf, focus, **kw)
