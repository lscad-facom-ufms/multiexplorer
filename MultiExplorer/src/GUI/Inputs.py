import Tkinter
import ttk

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
    def __init__(self, infra_group, master=None, cnf={}, **kw):
        super(InputGroupFrame, self).__init__(master, cnf, **kw)

        self.configure(
            relief='groove',
            labelanchor='n',
            text=infra_group.label,
        )

        self.infra_group = infra_group

        self.inputs = {}

        for key in infra_group.inputs:
            cur_input = infra_group.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                self.inputs[key] = InputGUI.create_input(cur_input, self)

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                self.inputs[key] = InputGUI.create_input_group(cur_input, self)

        self.pack()

    # todo
    def is_valid(self):
        """
        Returns True if all values from inputs and inputs subgroups that belong to this group are valid. False otherwise.
        """
        pass


class InputFrame(Tkinter.Frame, object):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(InputFrame, self).__init__(master, cnf, **kw)

        self.entry = None

        self.infra_input = infra_input

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=1)

        self.label = InputLabel(infra_input.get_label(), self)

        self.pack()

    def is_valid(self):
        self.infra_input.is_valid()


class InputLabel(Tkinter.Label, object):
    def __init__(self, label_text, master=None, cnf={}, **kw):
        super(InputLabel, self).__init__(master, cnf, **kw)

        self.configure(
            activebackground=DefaultStyleSettings.bg_color,
            text=label_text
        )

        self.grid(
            column=0,
            columnspan=3,
            row=0,
            rowspan=1,
        )


class SelectEntry(ttk.Combobox, object):
    def __init__(self, infra_input, master=None, **kw):
        super(SelectEntry, self).__init__(master, **kw)

        self.grid(
            column=3,
            columnspan=3,
            row=0,
            rowspan=1,
        )

        self.infra_input = infra_input

        self.bind("<<ComboboxSelected>>", self.set_input_value)

        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        validate_command = (self.register(self.on_validate),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.configure(
            state="readonly",
            values=list(infra_input.allowed_values.values()),
            validate="key",
            validatecommand=validate_command,
        )

    def on_validate(self, d, i, P, s, S, v, V, W):
        if self.infra_input.is_valid(S) is True:
            return True

        self.bell()

        return False

    def set_input_value(self, event):
        self.infra_input.set_value_from_gui(self.get())


class Select(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Select, self).__init__(infra_input, master, cnf, **kw)

        self.entry = SelectEntry(infra_input, self)


class TypeInEntry(Tkinter.Entry, object):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(TypeInEntry, self).__init__(master, cnf, **kw)

        self.configure(
            background=DefaultStyleSettings.input_bg_color,
            font=DefaultStyleSettings.input_font,
            selectbackground=DefaultStyleSettings.input_selected_bg_color,
            selectforeground=DefaultStyleSettings.input_selected_fg_color,
        )

        self.infra_input = infra_input

        self.bind("<FocusOut>", self.set_input_value)

        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        validate_command = (self.register(self.on_validate),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.configure(
            validate="key",
            validatecommand=validate_command,
        )

        self.grid(
            column=3,
            columnspan=3,
            row=0,
            rowspan=1,
        )

    def on_validate(self, d, i, P, s, S, v, V, W):
        if self.infra_input.is_valid(S) is True:
            return True

        self.bell()

        return False

    def set_input_value(self, event):
        self.infra_input.set_value_from_gui(self.get())


class Integer(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Integer, self).__init__(infra_input, master, cnf, **kw)

        self.infra_input = infra_input

        self.entry = TypeInEntry(infra_input, self)


class Float(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Float, self).__init__(infra_input, master, cnf, **kw)

        self.entry = TypeInEntry(infra_input, self)
