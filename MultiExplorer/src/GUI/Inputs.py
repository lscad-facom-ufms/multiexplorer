import Tkinter
import ttk

from Tkconstants import LEFT as SIDE_LEFT, TOP as SIDE_TOP
from MultiExplorer.src.GUI.Styles import DefaultStyle
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
        if infra_input.type == InputType.IntegerRange:
            return IntegerRange

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

    def is_valid(self):
        """
        Returns True if all values from inputs and inputs subgroups that belong to this group are valid. False
        otherwise.
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

    # todo
    def display_as_valid(self):
        pass

    # todo
    def display_as_invalid(self):
        pass

    def get_infra_input(self):
        return self.infra_group


class InputFrame(Tkinter.Frame, object):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(InputFrame, self).__init__(master, cnf, **kw)

        self.label = InputLabel(infra_input.get_label(), self)

        self.entry = None

        self.validation_label = ValidationLabel(None, self)

        self.infra_input = infra_input

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=1)

        self.pack()

    def is_valid(self):
        validation_result = self.infra_input.is_valid()

        if validation_result:
            self.display_as_valid()
        else:
            self.display_as_invalid()

        return validation_result

    def display_as_valid(self):
        self.validation_label.display_as_valid()

    def display_as_invalid(self):
        self.validation_label.display_as_invalid()

    def get_infra_input(self):
        return self.infra_input


class MultipleInputFrame(Tkinter.Frame, object):
    def __init__(self, conf, master=None, cnf={}, **kw):
        """
        conf = Dict {
            "infra_input" : Input,
            "number_of_entries": int,
            "labels": List[str],
        }
        """
        super(MultipleInputFrame, self).__init__(master, cnf, **kw)

        self.infra_input = conf['infra_input']  # type: Input

        self.number_of_entries = conf['number_of_entries']

        self.entries = []  # type: List[SubTypeInEntry]

        self.values = [None] * self.number_of_entries  # type: List[int]

        self.columnconfigure(0, weight=self.number_of_entries + len(conf['labels']) + 1)
        self.rowconfigure(0, weight=1)

        self.label = InputLabel(self.infra_input.get_label() + " - ", self)

        for indx in range(0, self.number_of_entries):
            self.entries.append(SubTypeInEntry(self, int(indx), conf['labels'][indx]))

        self.pack()

    def entry_is_valid(self, indx, value):
        # type: (int, str) -> bool
        new_values = self.values

        new_values[indx] = value

        self.infra_input.is_valid(tuple(new_values))

        return True

    def is_valid(self):
        # type: () -> bool
        return self.infra_input.is_valid(self.values)

    def set_entry_value(self, indx, value):
        # type: (int, str) -> None
        self.values[indx] = value

        self.set_input_value()

    def set_input_value(self):
        self.infra_input.set_value_from_gui(tuple(self.values))


class InputLabel(Tkinter.Label, object):
    def __init__(self, label_text, master=None, cnf={}, **kw):
        super(InputLabel, self).__init__(master, cnf, **kw)

        self.configure(
            activebackground=DefaultStyle.bg_color,
            text=label_text
        )

        self.grid(
            column=0,
            columnspan=1,
            row=0,
            rowspan=1,
        )


class ValidationLabel(Tkinter.Label, object):
    def __init__self(self, pos=None, master=None, cnf={}, **kw):
        super(ValidationLabel, self).__init__(master, cnf, **kw)

        self.img = None

        if pos is None:
            pos = (0, 2)

        self.configure(
            activebackground=DefaultStyle.bg_color,
            text=None
        )

        self.grid(
            row=pos[0],
            column=pos[1],
            columnspan=1,
            rowspan=1,
        )

    # todo
    def display_as_valid(self):
        pass

    # todo
    def display_as_invalid(self):
        pass


class SelectEntry(ttk.Combobox, object):
    def __init__(self, infra_input, master=None, **kw):
        super(SelectEntry, self).__init__(master, **kw)

        self.grid(
            column=1,
            columnspan=1,
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
            background=DefaultStyle.input_bg_color,
            font=DefaultStyle.input_font,
            selectbackground=DefaultStyle.input_selected_bg_color,
            selectforeground=DefaultStyle.input_selected_fg_color,
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
            column=1,
            columnspan=1,
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


class SubTypeInEntry(Tkinter.Entry, object):
    def __init__(self, master, indx, label_text, cnf={}, **kw):
        # type: (MultipleInputFrame, int, str, Dict, str**) -> None
        super(SubTypeInEntry, self).__init__(master, cnf, **kw)

        self.master = master

        self.indx = indx

        self.label = InputLabel(label_text, master)

        self.label.grid(
            column=1 + 2 * self.indx,
            columnspan=1,
            row=0,
            rowspan=1,
        )

        self.configure(
            background=DefaultStyle.input_bg_color,
            font=DefaultStyle.input_font,
            selectbackground=DefaultStyle.input_selected_bg_color,
            selectforeground=DefaultStyle.input_selected_fg_color,
        )

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
            column=1 + 2 * self.indx + 1,
            columnspan=1,
            row=0,
            rowspan=1,
        )

    def on_validate(self, d, i, P, s, S, v, V, W):
        if self.master.entry_is_valid(self.indx, S) is True:
            return True

        self.bell()

        return False

    def set_input_value(self, event):
        self.master.set_entry_value(self.indx, self.get())


class Integer(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Integer, self).__init__(infra_input, master, cnf, **kw)

        self.infra_input = infra_input

        self.entry = TypeInEntry(infra_input, self)


class Float(InputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(Float, self).__init__(infra_input, master, cnf, **kw)

        self.entry = TypeInEntry(infra_input, self)


class IntegerRange(MultipleInputFrame):
    def __init__(self, infra_input, master=None, cnf={}, **kw):
        super(IntegerRange, self).__init__({
            'infra_input': infra_input,
            'labels': ['from', 'to'],
            'number_of_entries': 2,
        }, master, cnf, **kw)
