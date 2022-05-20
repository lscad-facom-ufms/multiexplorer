import Tkinter

from Tkconstants import LEFT as SIDE_LEFT, TOP as SIDE_TOP
from MultiExplorer.src.GUI.Styles import DefaultStyleSettings
from MultiExplorer.src.Infrastructure.Inputs import InputType, InputGroup, Input


class InputGUI:
    def __init__(self):
        pass

    @staticmethod
    def create_input(infra_input, master=None):
        if isinstance(infra_input, InputGroup):
            return InputGUI.create_input_group(infra_input, master)

        input_class = InputGUI.resolve_class(infra_input)

        return input_class(infra_input, master)

    @staticmethod
    def create_input_group(infra_input, master=None):
        return InputGroupFrame(infra_input, master)

    @staticmethod
    def resolve_class(infra_input):
        if infra_input.allowed_values is not None:
            return Select
        if infra_input.type == InputType.Float:
            return Float
        if infra_input.type == InputType.Integer:
            return Integer

        raise NotImplementedError("The GUI counterpart of '" + str(infra_input.type) + "' is not implemented.")


class InputGroupFrame(Tkinter.LabelFrame, object):
    def __init__(self, input_group, master=None, cnf={}, **kw):
        super(InputGroupFrame, self).__init__(master, cnf, **kw)

        self.configure(
            relief='groove',
            labelanchor='n',
            text=input_group.label,
        )

        self.inputs = {}

        for key in input_group.inputs:
            cur_input = input_group.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                self.inputs[key] = InputGUI.create_input(cur_input, self)

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                self.inputs[key] = InputGUI.create_input_group(cur_input, self)

        self.pack()


class InputFrame(Tkinter.Frame, object):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(InputFrame, self).__init__(master, cnf, **kw)

        self.infra_input = infra_input

        self.label = InputLabel(infra_input.get_label(), self)

        self.pack()


class InputLabel(Tkinter.Label, object):
    def __init__(self, label_text, master=None, **kw):
        super(InputLabel, self).__init__(master, **kw)

        self.configure(
            activebackground=DefaultStyleSettings.bg_color,
            text=label_text
        )

        self.pack()


class Select(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Select, self).__init__(infra_input, master, cnf, **kw)


class Integer(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Integer, self).__init__(infra_input, master, cnf, **kw)

        self.entry = Tkinter.Entry(self)
        self.entry.place(height=20, relwidth=100, bordermode='ignore')
        self.entry.configure(
            background=DefaultStyleSettings.input_bg_color,
            font=DefaultStyleSettings.input_font,
            selectbackground=DefaultStyleSettings.input_selected_bg_color,
            selectforeground=DefaultStyleSettings.input_selected_fg_color,
        )

        self.entry.pack()
        
        self.pack()


class Float(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Float, self).__init__(infra_input, master, cnf, **kw)
