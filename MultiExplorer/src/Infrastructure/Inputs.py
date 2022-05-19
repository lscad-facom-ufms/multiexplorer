from enum import Enum

from MultiExplorer.src.Infrastructure.Validators import Validator


class InputType(Enum):
    Text = 1
    Integer = 2
    Float = 3
    Bool = 4
    IntegerArray = 5
    Bit = 6

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in InputType)


class Input:
    def __init__(self, options):
        self.label = 'Input Label'

        self.key = 'input_key'

        self.type = InputType.Text

        self.value = None

        self.validator = None

        self.allowed_values = None

        if 'key' in options:
            self.key = str(options['key'])

            self.label = str(options['key']).capitalize()

        if 'label' in options:
            self.label = str(options['label'])

        if 'type' in options:
            if not isinstance(options['type'], InputType):
                raise ValueError("The value of the parameter 'type' must belong to the InputType enumeration.")

            self.type = options['type']

        if 'allowed_values' in options:
            self.allowed_values = options['allowed_values']

        if 'validator' in options:
            if not isinstance(options['validator'], Validator):
                raise TypeError("Parameter 'validator' must implement the Validator interface.")

            self.type = options['validator']

        if 'value' in options:
            self.value = options['value']

            if not self.is_valid():
                raise ValueError("Value informed is invalid.")

    def get_label(self):
        return self.label

    def is_valid(self):
        if self.allowed_values is not None:
            return self.value in self.allowed_values

        if self.validator is None:
            return True

        return self.validator.is_valid(self.value)

    def value_are_loose(self):
        if self.allowed_values is None:
            return True

        return False

    def values_are_fixed(self):
        if self.allowed_values is not None:
            return True

        return False


class InputGroup:
    label = 'Group Label'

    key = 'group_key'

    inputs = {}

    def __init__(self, options):
        if 'label' in options:
            self.label = options['label']

        if 'inputs' in options:
            self.set_inputs(options['inputs'])

    def set_inputs(self, inputs):
        self.inputs = {}

        for i in inputs:
            if (not isinstance(i, Input)) and (not isinstance(i, InputGroup)):
                raise TypeError("Input groups can only contain either other input groups, or inputs")

            self.inputs[i.key] = i

    def get_label(self):
        return self.label

    def is_valid(self):
        for key in self.inputs:
            if not self.inputs[key].is_valid():
                return False

        return True
