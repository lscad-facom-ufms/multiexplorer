import Tkinter
import ttk

from Tkconstants import CENTER as ANCHOR_CENTER, DISABLED as STATE_DISABLED, NORMAL as STATE_NORMAL

from MultiExplorer.src.GUI.Inputs import InputGUI
from MultiExplorer.src.GUI.Menus import DefaultMenu
from MultiExplorer.src.GUI.Styles import DefaultStyle, DefaultStyleSettings
from MultiExplorer.src.Infrastructure.Registries import ExecutionFlowRegistry


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

        self.screens = {
            LoadScreen.__name__: LoadScreen(self),
            LaunchScreen.__name__: LaunchScreen(self, focus=True),
            InputScreen.__name__: InputScreen(self),
        }

    def get_screen(self, class_name):
        return self.screens[class_name]

    def navigate(self, from_screen, to_screen):
        from_screen.pack_forget()

        load_screen = self.get_screen(LoadScreen.__name__)

        load_screen.pack(fill="both", expand=True)

        from_screen.close_gracefully()

        to_screen.prepare()

        load_screen.pack_forget()

        to_screen.pack(fill="both", expand=True)


class ScreenFrame(Tkinter.Frame, object):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(ScreenFrame, self).__init__(master, cnf, **kw)

        if focus is True:
            self.pack(fill="both", expand=True)

    def navigate(self, to_screen):
        self.master.navigate(self, to_screen)

    def reset(self):
        pass

    def prepare(self):
        pass

    def close_gracefully(self):
        pass


class LoadScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(LoadScreen, self).__init__(master, cnf, focus, **kw)


class LaunchScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(LaunchScreen, self).__init__(master, cnf, focus, **kw)

        self.me_logo_image = Tkinter.Label(self)
        self.me_logo_image.place(relx=0.5, anchor="n", height=150, width=250)
        self.me_logo_image.configure(activebackground=DefaultStyleSettings.bg_color)
        self.me_logo_image.configure(text='''MultiExplorer.png''')

        self.execution_flow_label_frame = Tkinter.LabelFrame(self)
        self.execution_flow_label_frame.place(relx=0.5, rely=0.5, anchor=ANCHOR_CENTER, height=120, width=600)
        self.execution_flow_label_frame.configure(relief='groove')
        self.execution_flow_label_frame.configure(labelanchor='n')
        self.execution_flow_label_frame.configure(text='''Execution Flow''')

        self.execute_button = Tkinter.Button(
            self.execution_flow_label_frame,
            command=lambda: self.execute_flow(),
            state=STATE_DISABLED,
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
        self.select_execution_flow_combobox.bind('<<ComboboxSelected>>', self.enable_execution)
        self.select_execution_flow_combobox.configure(values=ExecutionFlowRegistry().get_flows_list())
        self.select_execution_flow_combobox.configure(takefocus="")

    def enable_execution(self, event):
        self.execute_button.config(state=STATE_NORMAL)

        self.selected_flow_label = self.select_execution_flow_combobox.get()

    def execute_flow(self):
        input_screen = self.master.get_screen(InputScreen.__name__)

        input_screen.reset()

        input_screen.set_flow(self.selected_flow_label)

        self.navigate(input_screen)


class InputScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(InputScreen, self).__init__(master, cnf, focus, **kw)

        self.title = Tkinter.Label(self)
        self.title.place(relx=0.5, anchor="n", height=50, relwidth=1)
        self.title.configure(activebackground=DefaultStyleSettings.bg_color)
        self.title.configure(text='''Execution Flow Settings''')

        self.tabs_controller = InputTabsController(self)

    def set_flow(self, flow_label):
        self.flow = ExecutionFlowRegistry().get_flow(flow_label)

        self.title.configure(text=self.flow.get_label()+''' Settings''')

    def reset_tabs(self):
        self.tabs_controller.destroy()

        self.tabs_controller = InputTabsController(self)

    def set_tabs(self):
        steps = self.flow.get_steps()

        for step_label in steps:
            self.tabs_controller.add_step_tab(steps[step_label])

    def prepare(self):
        self.reset_tabs()

        self.set_tabs()


class InputTabsController(ttk.Notebook, object):
    def __init__(self, master=None, **kw):
        super(InputTabsController, self).__init__(master, **kw)

        self.pack(fill="both", expand=True, pady=100, padx=50)

        self.tabs = {}

    def add_step_tab(self, step):
        if not step.has_user_input():
            return

        self.add(InputTab(step, self), text=step.get_label())


class InputTab(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(InputTab, self).__init__(master, cnf, **kw)

        self.inputs = {}

        step_user_inputs = step.get_user_inputs()

        for input_key in step_user_inputs:
            self.inputs[input_key] = InputGUI.create_input(step_user_inputs[input_key], self)

        self.pack(fill="both", expand=True)
