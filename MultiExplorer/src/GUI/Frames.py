import Tkinter
import ttk
import tkMessageBox

from Tkconstants import DISABLED as STATE_DISABLED, NORMAL as STATE_NORMAL
from Tkconstants import HORIZONTAL as HORIZONTAL_ORIENTATION, VERTICAL as VERTICAL_ORIENTATION
from Tkconstants import X as FILL_X, Y as FILL_Y, BOTH as FILL_BOTH
from Tkconstants import W as STICKY_WEST, E as STICKY_EAST
from Tkconstants import CENTER as ANCHOR_CENTER, NE as ANCHOR_NE, S as ANCHOR_SOUTH, W as ANCHOR_WEST
from Tkconstants import S as ANCHOR_S, N as ANCHOR_N, NW as ANCHOR_NW, SW as ANCHOR_SW, SE as ANCHOR_SE
from Tkconstants import BOTTOM as SIDE_BOTTOM, TOP as SIDE_TOP, LEFT as SIDE_LEFT, RIGHT as SIDE_RIGHT

from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow, Step
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.CPUHeterogeneousMulticoreExploration import \
    CPUHeterogeneousMulticoreExplorationExecutionFlow
from MultiExplorer.src.GUI.Buttons import NavigateButton
from MultiExplorer.src.GUI.Inputs import InputGUI
from MultiExplorer.src.GUI.Menus import DefaultMenu
from MultiExplorer.src.GUI.Styles import DefaultStyle
from MultiExplorer.src.GUI.Widgets import ScreenTitle, CanvasFrame, WrappingLabel, CanvasTable
from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.Registries import ExecutionFlowRegistry
from matplotlib.figure import Figure as MatplotFigure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, Optional, List


class MainWindow(Tkinter.Tk, object):
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super(MainWindow, self).__init__(screenName, baseName, className, useTk, sync, use)

        self.geometry("1024x768")

        self.minsize(640, 480)

        self.maxsize(1920, 1080)

        self.resizable(1, 1)

        self.title("MultiExplorer")

        self.configure(highlightcolor="black")

        self.style = DefaultStyle()

        self.update()

        # self.menu = DefaultMenu(self)

        self.screens = {
            LoadScreen.__name__: LoadScreen(self),
            LaunchScreen.__name__: LaunchScreen(self, focus=True),
            InputScreen.__name__: InputScreen(self),
            ExecutionScreen.__name__: ExecutionScreen(self),
            ResultScreen.__name__: ResultScreen(self),
        }

    def get_screen(self, class_name):
        return self.screens[class_name]

    def navigate(self, from_screen, to_screen, **kw):
        from_screen.pack_forget()

        load_screen = self.get_screen(LoadScreen.__name__)

        load_screen.pack(fill=FILL_BOTH, expand=True)

        from_screen.close_gracefully()

        to_screen.prepare(**kw)

        load_screen.pack_forget()

        to_screen.pack(fill=FILL_BOTH, expand=True)

        to_screen.ready(**kw)


class ScreenFrame(Tkinter.Frame, object):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(ScreenFrame, self).__init__(master, cnf, **kw)

        if focus is True:
            self.pack(fill=FILL_BOTH, expand=True)

    def navigate(self, to_screen, **kw):
        self.master.navigate(self, to_screen, **kw)

    def navigate_by_class_name(self, to_screen_class_name, **kw):
        self.navigate(self.master.get_screen(to_screen_class_name), **kw)

    def reset(self):
        pass

    def prepare(self, **kw):
        pass

    def ready(self, **kw):
        pass

    def close_gracefully(self):
        pass


class LoadScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(LoadScreen, self).__init__(master, cnf, focus, **kw)


class FlowPreview(Tkinter.Frame, object):
    HEIGHT = 200

    WIDTH = 500

    STEP_WIDTH = 150

    def __init__(self, master=None, cnf={}, **kw):
        super(FlowPreview, self).__init__(master, cnf, **kw)

        self.canvas = None

        self.x_scroll = None

    def draw_flow(self, flow):
        # type: (ExecutionFlow) -> None
        steps = flow.get_steps()

        nbr_of_steps = len(steps)

        canvas_width = nbr_of_steps * FlowPreview.STEP_WIDTH

        if self.canvas:
            self.canvas.destroy()

            self.canvas = None

        if self.x_scroll:
            self.x_scroll.destroy()

            self.x_scroll = None

        self.canvas = Tkinter.Canvas(self, {
            'width': canvas_width,
        })

        self.canvas.pack(
            fill=FILL_BOTH,
            expand=True,
            side=SIDE_TOP,
        )

        self.x_scroll = Tkinter.Scrollbar(self, orient=HORIZONTAL_ORIENTATION)

        self.x_scroll.config(
            command=self.canvas.xview
        )

        self.x_scroll.pack(
            fill=FILL_X,
            expand=True,
            side=SIDE_BOTTOM,
        )

        self.canvas.config(
            bg=DefaultStyle.bg_color,
            xscrollcommand=self.x_scroll.set,
        )

        pad_x = (FlowPreview.WIDTH - canvas_width) / (nbr_of_steps + 1)

        x = pad_x

        y = FlowPreview.HEIGHT / 2

        for step in steps:
            self.draw_step(step, x, y)

            x = x + FlowPreview.STEP_WIDTH + pad_x

    def draw_step(self, step, x, y):
        # type: (Step, int, int) -> None
        self.canvas.create_polygon(
            [
                x + 0, y + 0,
                x + 12, y + 25,
                x, y + 50,
                x + 100, y + 50,
                x + 112, y + 25,
                x + 100, y,
                x, y
            ],
            fill=DefaultStyle.bg_color,
            outline=DefaultStyle.fg_color,
        )

        self.canvas.create_text(x + 56, y + 25, text=step.get_label(), anchor=ANCHOR_CENTER, font=('Helvetica', '7'),
                                width=80)


class LaunchScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(LaunchScreen, self).__init__(master, cnf, focus, **kw)

        self.selected_flow_label = None
        # todo We still lack a LOGO IMAGE
        # self.me_logo_image = Tkinter.Label(self)
        # self.me_logo_image.place(relx=0.5, anchor="n", height=150, width=250)
        # self.me_logo_image.configure(activebackground=DefaultStyleSettings.bg_color)
        # self.me_logo_image.configure(text='''MultiExplorer.png''')

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)

        self.rowconfigure(1, weight=2)

        self.execution_flow_label_frame = Tkinter.LabelFrame(self)

        self.execution_flow_label_frame.grid(
            column=0,
            row=1
        )

        self.execution_flow_label_frame.configure(
            relief='groove',
            labelanchor='n',
            text='''Start an Execution Flow''',
        )

        self.execution_flow_label_frame.rowconfigure(0, weight=1)
        self.execution_flow_label_frame.rowconfigure(1, weight=1)
        self.execution_flow_label_frame.rowconfigure(2, weight=1)
        self.execution_flow_label_frame.columnconfigure(0, weight=1)
        self.execution_flow_label_frame.columnconfigure(1, weight=1)

        self.select_execution_flow_combobox = ttk.Combobox(self.execution_flow_label_frame)

        self.select_execution_flow_combobox.configure(
            values=ExecutionFlowRegistry().get_flows_list(),
            takefocus="",
            width=40,
        )

        self.select_execution_flow_combobox.grid(
            column=0,
            row=0,
        )

        self.select_execution_flow_combobox.bind('<<ComboboxSelected>>', self.enable_execution)

        self.flow_info_area = Tkinter.Label(self.execution_flow_label_frame, {
            'wraplength': 500
        })

        self.execute_button = Tkinter.Button(
            self.execution_flow_label_frame,
            command=lambda: self.execute_flow(),
            state=STATE_DISABLED,
        )

        self.execute_button.configure(
            activebackground=DefaultStyle.button_active_bg_color,
            borderwidth=DefaultStyle.button_border_width,
            text='''Start'''
        )

        self.execute_button.grid(
            column=1,
            row=0,
        )

        self.flow_preview = FlowPreview(self.execution_flow_label_frame)

        self.flow_preview.grid(
            column=0,
            row=2,
        )

    def enable_execution(self, event):
        self.execute_button.config(state=STATE_NORMAL)

        self.selected_flow_label = self.select_execution_flow_combobox.get()

        self.display_flow_info()

    def display_flow_info(self):
        selected_flow_label = self.select_execution_flow_combobox.get()

        flow = ExecutionFlowRegistry().get_flow(selected_flow_label)

        flow_info = flow.get_info()

        if flow_info:
            self.flow_info_area.config(text=flow_info)

            self.flow_info_area.grid(
                column=0,
                row=1,
            )
        else:
            self.flow_info_area.config(text="")

            self.flow_info_area.grid_forget()

        self.flow_preview.draw_flow(flow)

    def execute_flow(self):
        input_screen = self.master.get_screen(InputScreen.__name__)

        input_screen.reset()

        input_screen.set_flow(self.selected_flow_label)

        self.navigate(input_screen)


class InputTab(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        super(InputTab, self).__init__(master, cnf, **kw)

        self.img = None

        self.step = step

        self.inputs = {}

        step_user_inputs = step.get_user_inputs()

        for input_key in step_user_inputs:
            self.inputs[input_key] = InputGUI.create_input(step_user_inputs[input_key], self)

        self.info_display = Tkinter.Frame(self)

        self.pack(fill=FILL_BOTH, expand=True)

        self.info_display.input_label = WrappingLabel(self.info_display)

        self.info_display.text = WrappingLabel(self.info_display)

        self.info_display.canvas_frame = CanvasFrame(self.info_display)

    def get_infra_inputs(self):
        infra_inputs = {}

        for key in self.inputs:
            infra_inputs[key] = self.inputs[key].get_infra_input()

        return infra_inputs

    def is_valid(self):
        """
        Verify each input and input group for validity.
        Returns True if all inputs are valid, and False otherwise.
        """
        all_valid = True
        for key in self.inputs:
            if self.inputs[key].is_valid():
                pass
            else:
                all_valid = False
        if all_valid:
            self.display_as_valid()

            return True
        else:
            self.display_as_invalid()

            return False

    def display_as_valid(self):
        self.img = DefaultStyle.get_image("check.png", (10, 10))

        self.master.tab(
            self.master.index(self),
            text=self.step.get_label(),
            image=self.img,
            compound=Tkinter.LEFT,
        )

    def display_as_invalid(self):
        self.img = DefaultStyle.get_image("close.png", (10, 10))

        self.master.tab(
            self.master.index(self),
            text=self.step.get_label(),
            image=self.img,
            compound=Tkinter.LEFT,
        )

        self.master.select(self.master.index(self))

    def show_additional_info(self, label, additional_info):
        self.info_display.pack(fill=FILL_X, expand=True)

        if 'text' in additional_info:
            self.info_display.text.config(text=additional_info['text'])

            self.info_display.text.pack()
        else:
            self.info_display.text.pack_forget()

        self.info_display.canvas_frame.canvas.delete("all")

        if 'table_data' in additional_info:
            self.info_display.canvas_frame.pack(fill=FILL_BOTH, expand=True)

            CanvasTable(self.info_display.canvas_frame.canvas, additional_info['table_data'])
        else:
            self.info_display.canvas_frame.pack_forget()

    # todo
    def hide_additional_info(self):
        self.info_display.pack_forget()


class InputTabsController(ttk.Notebook, object):
    def __init__(self, master=None, **kw):
        super(InputTabsController, self).__init__(master, **kw)

        self.input_tabs = []

        self.pack(fill=FILL_BOTH, expand=True, pady=100, padx=50)

    def add_step_tab(self, step):
        if not step.has_user_input():
            return

        input_tab = InputTab(step, self)

        self.add(input_tab, text=step.get_label())

        self.input_tabs.append(input_tab)

    def get_infra_inputs_per_step(self):
        infra_inputs_per_step = {}

        for tab in self.input_tabs:
            infra_inputs_per_step[tab.step.get_label()] = tab.get_infra_inputs()

        return infra_inputs_per_step

    def is_valid(self):
        """
        Must verify all values from all inputs, from each tab.
        Returns true if all input values are valid; returns false otherwise.
        """
        all_tabs_are_valid = True

        for input_tab in self.input_tabs:
            if not input_tab.is_valid():
                all_tabs_are_valid = False

        return all_tabs_are_valid


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
            activebackground=DefaultStyle.button_active_bg_color,
            borderwidth=DefaultStyle.button_border_width,
            text='''Execute'''
        )

    def set_flow(self, flow_label):
        self.flow_label = flow_label

        self.flow = ExecutionFlowRegistry().get_flow(flow_label)

        self.title.configure(text=self.flow.get_label() + ''' Settings''')

    def execute_flow(self):
        if self.tabs_controller.is_valid():
            execution_screen = self.master.get_screen(ExecutionScreen.__name__)

            execution_screen.set_flow(self.flow_label)

            self.navigate(execution_screen, execute=True)

    def get_infra_inputs_per_step(self):
        return self.tabs_controller.get_infra_inputs_per_step()

    def reset_tabs(self):
        self.tabs_controller.destroy()

        self.tabs_controller = InputTabsController(self)

    def set_tabs(self):
        steps = self.flow.get_steps()

        for step in steps:
            self.tabs_controller.add_step_tab(step)

    def update_tabs(self):
        print self

    def prepare(self, **kw):
        self.reset_tabs()

        self.set_tabs()

        self.update()


class InputInfo(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        super(InputInfo, self).__init__(master, cnf, **kw)


class StepButtons(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        super(StepButtons, self).__init__(master, cnf, **kw)

        self.step = step

        self.step.add_handler(Event.STEP_EXECUTION_ENDED, self.show_result_buttons)

        self.see_results = Tkinter.Button(
            self,
            text="Preview Results",
            command=self.preview_results,
        )

    def show_result_buttons(self):
        self.see_results.pack()

    def preview_results(self):
        self.master.preview_results()


class StepResults(Tkinter.Frame, object):
    def __init__(self, step, master=None, cnf={}, **kw):
        super(StepResults, self).__init__(master, cnf, **kw)

        self.step = step

    def preview_results(self):
        presenter = self.step.get_presenter()

        results = self.step.get_results()

        if presenter is not None and results is not None:
            tkMessageBox.showinfo(
                "Preview " + self.step.get_label() + " Results",
                presenter.get_info(results),
            )
        else:
            tkMessageBox.showinfo(
                "Preview " + self.step.get_label() + " Results",
                "Unavailable",
            )


class StepFrame(Tkinter.Frame, object):
    HEIGHT = 400

    WIDTH = 300

    def __init__(self, step, master=None, cnf={}, **kw):
        super(StepFrame, self).__init__(master, cnf, **kw)

        self.config(
            height=StepFrame.HEIGHT,
            width=StepFrame.WIDTH,
        )

        self.pack(
            side=SIDE_LEFT,
        )

        self.canvas = Tkinter.Canvas(self)

        self.canvas.config(
            height=StepFrame.HEIGHT / 3.0,
            width=StepFrame.WIDTH,
        )

        self.canvas.pack(
            anchor=ANCHOR_CENTER,
        )

        self.step_display = StepDisplay(
            step,
            self.canvas,
            (StepFrame.WIDTH / 2) - 112.5,
            ((StepFrame.HEIGHT / 3.0) / 2) - 50
        )

        self.step_buttons = StepButtons(step, self)

        self.step_buttons.config(
            height=50,
            width=StepFrame.WIDTH,
        )

        self.step_buttons.pack(
            side=SIDE_BOTTOM,
        )

        self.step_results = StepResults(step, self)

    def preview_results(self):
        self.step_results.preview_results()


class StepDisplay(object):
    def __init__(self, step, canvas, x, y):
        self.step = step

        self.step.add_handler(Event.STEP_EXECUTION_STARTED, self.start_execution_animation)

        self.step.add_handler(Event.STEP_EXECUTION_ENDED, self.stop_execution_animation)

        self.step.add_handler(Event.STEP_EXECUTION_FAILED, self.stop_execution_animation)

        self.is_executing = False

        self.animation_job = None

        self.execution_job = None

        self.canvas = canvas

        self.label_id = None

        self.shape_id = self.create_step_shape(x, y)

    def start_execution_animation(self, *args):
        self.is_executing = True

        self.animation_job = self.canvas.after(500, self.blink, True)

        self.execution_job = self.canvas.after(500, self.check_step_execution)

    def check_step_execution(self):
        if not self.step.is_finished():
            self.execution_job = self.canvas.after(500, self.check_step_execution)

    def stop_execution_animation(self, *args):
        if self.animation_job is not None:
            self.canvas.after_cancel(self.animation_job)

        if self.execution_job is not None:
            self.canvas.after_cancel(self.execution_job)

        self.is_executing = False

        self.canvas.itemconfig(self.shape_id, fill=DefaultStyle.bg_color)

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
            fill=DefaultStyle.bg_color,
            outline=DefaultStyle.fg_color,
        )

        self.label_id = self.canvas.create_text(x + 112, y + 50, text=self.step.get_label(), anchor=ANCHOR_CENTER)

        return step_shape_id

    def blink(self, blink_ctrl):
        if blink_ctrl is True:
            self.canvas.itemconfig(self.shape_id, fill=DefaultStyle.active_color)

            blink_ctrl = False
        else:
            self.canvas.itemconfig(self.shape_id, fill=DefaultStyle.bg_color)

            blink_ctrl = True

        if self.is_executing:
            self.animation_job = self.canvas.after(500, self.blink, blink_ctrl)


class ExecutionDisplay(Tkinter.Canvas, object):
    HEIGHT = 400

    def __init__(self, master=None, cnf={}, **kw):
        super(ExecutionDisplay, self).__init__(master, cnf, **kw)

        self.master = master

        self.frame_id = None

        self.frame = None

        self.execution_flow = None

        self.step_frames = {}

        self.scrollbar = Tkinter.Scrollbar(master, orient=HORIZONTAL_ORIENTATION)

        self.scrollbar.pack(
            fill=FILL_X,
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
            bg=DefaultStyle.bg_color,
            xscrollcommand=self.scrollbar.set,
        )

    def set_execution_flow(self, flow):
        self.execution_flow = flow

        self.delete('all')

        self.draw()

    def draw(self):
        if self.frame_id is not None:
            self.delete(self.frame_id)

        steps = self.execution_flow.get_steps()

        self.frame = Tkinter.Frame(self.master)

        step_nbr = 0
        for step in steps:
            self.add_step_frame(step)

            step_nbr += 1

        new_width = step_nbr * StepFrame.WIDTH

        self.frame.config(
            height=ExecutionDisplay.HEIGHT,
            width=new_width,
        )

        self.frame_id = self.create_window(
            0,
            0,
            window=self.frame,
            anchor=ANCHOR_NW,
        )

        self.config(
            scrollregion=(0, 0, new_width, ExecutionDisplay.HEIGHT),
        )

        self.xview('moveto', '0.0')

    def add_step_frame(self, step):
        self.step_frames[step.get_label()] = StepFrame(step, self.frame)


class ExecutionScreen(ScreenFrame):
    DISPLAY_AREA_HEIGHT = 400

    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(ExecutionScreen, self).__init__(master, cnf, focus, **kw)

        self.flow_label = None
        self.flow = None

        self.title = Tkinter.Label(self)
        self.title.place(relx=0.5, anchor="n", height=50, relwidth=1)
        self.title.configure(activebackground=DefaultStyle.bg_color)
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

        self.results_button = NavigateButton(ResultScreen.__name__, self, self.button_area, {
            'text': 'See Results',
            'state': STATE_DISABLED,
        })

        self.results_button.grid(
            column=1,
            row=0,
            sticky=STICKY_EAST,
            padx=50
        )

        self.display_area = Tkinter.Frame(self)

        self.display_area.config(
            height=ExecutionScreen.DISPLAY_AREA_HEIGHT,
        )

        self.display_area.pack(
            fill='x',
            expand=True,
            side=SIDE_BOTTOM,
            padx=DefaultStyle.padx,
        )

        self.execution_display = ExecutionDisplay(self.display_area)

    def set_flow(self, flow_label):
        self.flow_label = flow_label

        self.flow = ExecutionFlowRegistry().get_flow(flow_label)

        self.execution_display.set_execution_flow(self.flow)

        self.title.configure(text=self.flow.get_label() + ''' Execution''')

        self.flow.add_handler(Event.FLOW_EXECUTION_ENDED, self.show_results)

        result_screen = self.master.get_screen(ResultScreen.__name__)

        result_screen.set_flow(self.flow)

    def show_results(self):
        self.results_button.config(state=STATE_NORMAL)

        # result_screen = self.master.get_screen(ResultScreen.__name__)
        #
        # self.navigate(result_screen)

    def prepare(self, **kw):
        input_screen = self.master.get_screen(InputScreen.__name__)

        infra_inputs_per_step = input_screen.get_infra_inputs_per_step()

        for step in self.flow.steps:
            if step.has_user_input():
                step.copy_input_values(infra_inputs_per_step[step.get_label()])

    def ready(self, execute=False):
        if execute:
            self.flow.execute()


class ResultScreen(ScreenFrame):
    def __init__(self, master=None, cnf={}, focus=False, **kw):
        super(ResultScreen, self).__init__(master, cnf, focus, **kw)

        self.flow = None  # type: Optional[ExecutionFlow]

        self.presentation_frames = None  # type: Optional[List[Tkinter.Frame]]

        self.configure(
            padx=50,
            pady=50,
        )

        self.update()

        total_height = master.winfo_height()

        total_width = master.winfo_width()

        self.container = Tkinter.Frame(self)

        self.container.pack(
            side=SIDE_TOP,
        )

        self.scroll_area = Tkinter.Canvas(
            self.container,
            width=total_width - 116,
            height=total_height - 200,
        )

        self.scroll_area.pack(
            side=SIDE_LEFT,
        )

        self.y_scroll = Tkinter.Scrollbar(self.container, orient=Tkinter.VERTICAL)

        self.y_scroll.pack(
            side=SIDE_RIGHT,
            fill='y',
            expand=True,
        )

        self.y_scroll.config(
            command=self.scroll_area.yview
        )

        self.scroll_area.config(
            yscrollcommand=self.y_scroll.set,
        )

        self.scroll_width = total_width - 116

        self.scroll_area.config(
            scrollregion=(0, 0, self.scroll_width, 0)
        )

        self.scroll_area.yview('moveto', '0.0')

        self.flow = None

        self.button_area = Tkinter.Frame(self, width=total_width - 100)

        self.button_area.pack(
            side=SIDE_TOP,
        )

        self.button_area.columnconfigure(0, weight=1)
        self.button_area.columnconfigure(1, weight=1)
        self.button_area.rowconfigure(0, weight=1)

        self.back_button = NavigateButton(ExecutionScreen.__name__, self, self.button_area, {
            'text': 'Back',
        })

        self.back_button.grid(
            column=0,
            row=0,
            sticky=STICKY_WEST,
        )

    def reset(self):
        self.scroll_area.delete('presentation')

    def set_flow(self, flow):
        # type: (ExecutionFlow) -> None
        self.flow = flow

    def prepare(self, **kw):
        self.present_results()

    def present_results(self):
        self.presentation_frames = []

        total_height = 0

        results = self.flow.get_results()

        for presenter in self.flow.get_presenters():
            presentation_frame = Tkinter.Frame(self.scroll_area, width=self.scroll_width-20, padx=10)

            presentation_frame.pack(side=SIDE_TOP)

            self.presentation_frames.append(presentation_frame)

            self.scroll_area.create_window(
                0, total_height, window=presentation_frame, anchor=ANCHOR_NW, tags='presentation'
            )

            total_height = total_height + presenter.present_results(presentation_frame, results, {
                'width': self.scroll_width-20,
            }) + 10

        self.scroll_area.config(
            scrollregion=(0, 0, self.scroll_width, total_height)
        )

        self.scroll_area.yview('moveto', '0.0')

    def close_gracefully(self):
        self.reset()
