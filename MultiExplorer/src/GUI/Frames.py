import Tkinter
import ttk

from Tkconstants import DISABLED as STATE_DISABLED, NORMAL as STATE_NORMAL
from Tkconstants import HORIZONTAL as HORIZONTAL_ORIENTATION
from Tkconstants import BOTH as FILL_BOTH
from Tkconstants import W as STICKY_WEST, E as STICKY_EAST
from Tkconstants import CENTER as ANCHOR_CENTER
from Tkconstants import S as ANCHOR_S, N as ANCHOR_N, SW as ANCHOR_SW, SE as ANCHOR_SE
from Tkconstants import BOTTOM as SIDE_BOTTOM, TOP as SIDE_TOP, LEFT as SIDE_LEFT

from MultiExplorer.src.GUI.Buttons import NavigateButton
from MultiExplorer.src.GUI.Inputs import InputGUI
from MultiExplorer.src.GUI.Menus import DefaultMenu
from MultiExplorer.src.GUI.Styles import DefaultStyle, DefaultStyleSettings
from MultiExplorer.src.GUI.Widgets import ScreenTitle
from MultiExplorer.src.Infrastructure.Events import Event
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
            ExecutionScreen.__name__: ExecutionScreen(self),
        }

    def get_screen(self, class_name):
        return self.screens[class_name]

    def navigate(self, from_screen, to_screen):
        from_screen.pack_forget()

        load_screen = self.get_screen(LoadScreen.__name__)

        load_screen.pack(fill=FILL_BOTH, expand=True)

        from_screen.close_gracefully()

        to_screen.prepare()

        load_screen.pack_forget()

        to_screen.pack(fill=FILL_BOTH, expand=True)

        to_screen.ready()


class ScreenFrame(Tkinter.Frame, object):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(ScreenFrame, self).__init__(master, cnf, **kw)

        if focus is True:
            self.pack(fill=FILL_BOTH, expand=True)

    def navigate(self, to_screen):
        self.master.navigate(self, to_screen)

    def navigate_by_class_name(self, to_screen_class_name):
        self.navigate(self.master.get_screen(to_screen_class_name))

    def reset(self):
        pass

    def prepare(self):
        pass

    def ready(self):
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

        self.selected_flow_label = None
        self.me_logo_image = Tkinter.Label(self)
        self.me_logo_image.place(relx=0.5, anchor="n", height=150, width=250)
        self.me_logo_image.configure(activebackground=DefaultStyleSettings.bg_color)
        self.me_logo_image.configure(text='''MultiExplorer.png''')

        self.execution_flow_label_frame = Tkinter.LabelFrame(self)

        self.execution_flow_label_frame.place(
            relx=0.5,
            rely=0.5,
            anchor=ANCHOR_CENTER
        )

        self.execution_flow_label_frame.configure(
            relief='groove',
            labelanchor='n',
            text='''Execution Flow''',
        )

        self.execution_flow_label_frame.rowconfigure(0, weight=1)
        self.execution_flow_label_frame.columnconfigure(0, weight=1)

        self.select_execution_flow_combobox = ttk.Combobox(self.execution_flow_label_frame)

        self.select_execution_flow_combobox.grid(
            column=0,
            row=0,
        )

        self.select_execution_flow_combobox.bind('<<ComboboxSelected>>', self.enable_execution)

        self.select_execution_flow_combobox.configure(
            values=ExecutionFlowRegistry().get_flows_list(),
            takefocus="",
        )

        self.execute_button = Tkinter.Button(
            self.execution_flow_label_frame,
            command=lambda: self.execute_flow(),
            state=STATE_DISABLED,
        )

        self.execute_button.grid(
            column=1,
            row=0,
        )

        self.execute_button.configure(
            activebackground=DefaultStyleSettings.button_active_bg_color,
            borderwidth=DefaultStyleSettings.button_border_width,
            text='''Start'''
        )

    def enable_execution(self, event):
        self.execute_button.config(state=STATE_NORMAL)

        self.selected_flow_label = self.select_execution_flow_combobox.get()

    def execute_flow(self):
        input_screen = self.master.get_screen(InputScreen.__name__)

        input_screen.reset()

        input_screen.set_flow(self.selected_flow_label)

        self.navigate(input_screen)


class InputTab(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        super(InputTab, self).__init__(master, cnf, **kw)

        self.inputs = {}

        step_user_inputs = step.get_user_inputs()

        for input_key in step_user_inputs:
            self.inputs[input_key] = InputGUI.create_input(step_user_inputs[input_key], self)

        self.pack(fill=FILL_BOTH, expand=True)


class InputTabsController(ttk.Notebook, object):
    def __init__(self, master=None, **kw):
        super(InputTabsController, self).__init__(master, **kw)

        self.pack(fill=FILL_BOTH, expand=True, pady=100, padx=50)

        self.tabs = {}

    def add_step_tab(self, step):
        if not step.has_user_input():
            return

        self.add(InputTab(step, self), text=step.get_label())


class InputScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(InputScreen, self).__init__(master, cnf, focus, **kw)

        self.flow_label = None
        self.flow = None

        self.title = ScreenTitle("Execution Flow Settings", self)

        self.tabs_controller = InputTabsController(self)

        self.button_area = Tkinter.Frame(self)

        self.button_area.pack(
            side=SIDE_BOTTOM,
            fill='x',
            expand=True,
        )

        self.button_area.columnconfigure(0, weight=1)
        self.button_area.columnconfigure(1, weight=1)
        self.button_area.rowconfigure(0, weight=1)

        self.back_button = NavigateButton(LaunchScreen.__name__, self, self.button_area, {
            'text': 'Back',
        })

        self.back_button.grid(
            column=0,
            row=0,
            sticky=STICKY_WEST,
            padx=50,
        )

        self.execute_button = Tkinter.Button(
            self.button_area,
            command=lambda: self.execute_flow(),
        )

        self.execute_button.grid(
            column=1,
            row=0,
            sticky=STICKY_EAST,
            padx=50,
        )

        self.execute_button.configure(
            activebackground=DefaultStyleSettings.button_active_bg_color,
            borderwidth=DefaultStyleSettings.button_border_width,
            text='''Execute'''
        )

    def set_flow(self, flow_label):
        self.flow_label = flow_label

        self.flow = ExecutionFlowRegistry().get_flow(flow_label)

        self.title.configure(text=self.flow.get_label() + ''' Settings''')

    def execute_flow(self):
        execution_screen = self.master.get_screen(ExecutionScreen.__name__)

        execution_screen.set_flow(self.flow_label)

        self.navigate(execution_screen)

    def reset_tabs(self):
        self.tabs_controller.destroy()

        self.tabs_controller = InputTabsController(self)

    def set_tabs(self):
        steps = self.flow.get_steps()

        for step in steps:
            self.tabs_controller.add_step_tab(step)

    def prepare(self):
        self.reset_tabs()

        self.set_tabs()


class InputInfo(Tkinter.Frame, object):
    pass


class StepDisplay(object):
    def __init__(self, step, canvas, x, y):
        self.step = step

        self.step.add_handler(Event.EXECUTION_STARTED, self.start_execution_animation)

        self.step.add_handler(Event.EXECUTION_ENDED, self.stop_execution_animation)

        self.is_executing = False

        self.animation_job = None

        self.canvas = canvas

        self.shape_id = self.create_step_shape(x, y)

    def start_execution_animation(self):
        self.is_executing = True

        self.animation_job = self.canvas.after(500, self.blink, True)

        self.execution_job = self.canvas.after(500, self.check_step_execution)

    def check_step_execution(self):
       if not self.step.is_finished():
           self.execution_job = self.canvas.after(500, self.check_step_execution)

    def stop_execution_animation(self):
        self.is_executing = False

        if self.animation_job is not None:
            self.canvas.after_cancel(self.animation_job)

        if self.execution_job is not None:
            self.canvas.after_cancel(self.execution_job)

    def create_step_shape(self, x, y):
        step_shape_id = self.canvas.create_polygon(
            [
                x + 0, y + 0,
                x + 25, y + 50,
                x, y + 100,
                x + 200, y + 100,
                x + 225, y + 50,
                x + 200, y,
                x, y
            ],
            fill=DefaultStyleSettings.bg_color,
            outline=DefaultStyleSettings.fg_color,
        )

        return step_shape_id

    def blink(self, blink_ctrl):
        if blink_ctrl is True:
            self.canvas.itemconfig(self.shape_id, fill=DefaultStyleSettings.active_color)

            blink_ctrl = False
        else:
            self.canvas.itemconfig(self.shape_id, fill=DefaultStyleSettings.bg_color)

            blink_ctrl = True

        if self.is_executing:
            self.animation_job = self.canvas.after(500, self.blink, blink_ctrl)


class ExecutionDisplay(Tkinter.Canvas, object):
    def __init__(self, master=None, cnf={}, **kw):
        super(ExecutionDisplay, self).__init__(master, cnf, **kw)

        self.execution_flow = None
        self.step_displays = {}

        self.scrollbar = Tkinter.Scrollbar(master, orient=HORIZONTAL_ORIENTATION)

        self.scrollbar.pack(
            fill='x',
            expand=True,
            side=SIDE_BOTTOM,
        )

        self.scrollbar.config(
            command=self.xview
        )

        self.pack(
            fill=FILL_BOTH,
            expand=True,
            side=SIDE_LEFT,
        )

        self.config(
            bg=DefaultStyleSettings.bg_color,
            xscrollcommand=self.scrollbar.set,
            scrollregion=(0, 0, 700, 200),
        )

        self.y = 75

    def set_execution_flow(self, flow):
        self.execution_flow = flow

        self.delete('all')

        self.draw()

    def draw(self):
        self.step_display = []

        self.delete("all")

        self.x = 75

        steps = self.execution_flow.get_steps()

        for step in steps:
            self.add_step_display(step)

            self.x += 75

    def add_step_display(self, step):
        self.step_displays[step.get_label()] = StepDisplay(step, self, self.x, self.y)


class ExecutionScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(ExecutionScreen, self).__init__(master, cnf, focus, **kw)

        self.flow_label = None
        self.flow = None

        self.title = Tkinter.Label(self)
        self.title.place(relx=0.5, anchor="n", height=50, relwidth=1)
        self.title.configure(activebackground=DefaultStyleSettings.bg_color)
        self.title.configure(text='''Flow Execution''')

        self.input_info = InputInfo(self)

        self.button_area = Tkinter.Frame(self)

        self.button_area.pack(
            side=SIDE_BOTTOM,
            fill='x',
            expand=True,
        )

        self.button_area.columnconfigure(0, weight=1)
        self.button_area.columnconfigure(1, weight=1)
        self.button_area.rowconfigure(0, weight=1)

        self.back_button = NavigateButton(InputScreen.__name__, self, self.button_area, {
            'text': 'Back',
        })

        self.back_button.grid(
            column=0,
            row=0,
            sticky=STICKY_WEST,
            padx=50,
        )

        self.display_area = Tkinter.Frame(self)

        self.display_area.config(
            height=200,
            borderwidth=2,
            relief="sunken",
        )

        self.display_area.pack(
            fill='x',
            expand=True,
            side=SIDE_BOTTOM,
            padx=DefaultStyleSettings.padx,
        )

        self.execution_display = ExecutionDisplay(self.display_area)

    def set_flow(self, flow_label):
        self.flow_label = flow_label

        self.flow = ExecutionFlowRegistry().get_flow(flow_label)

        self.execution_display.set_execution_flow(self.flow)

        self.title.configure(text=self.flow.get_label() + ''' Execution''')

    def ready(self):
        self.flow.execute()
