import copy
from enum import Enum
from typing import Optional, Any, Dict, Union
from MultiExplorer.src.Infrastructure.Validators import Validator, IntegerValidator, FloatValidator


class InputType(Enum):
    Text = 1
    Integer = 2
    Float = 3
    Bool = 4
    IntegerArray = 5
    Bit = 6
    IntegerRange = 7

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in InputType)

    @staticmethod
    def get_default_validator(input_type):
        # type: (InputType) -> Optional[Validator]
        if input_type == InputType.Integer:
            return IntegerValidator()

        if input_type == InputType.Float:
            return FloatValidator()

        return None


class Input:
    def __init__(self, options):
        """
        options = Dict {
            "label" : str,
            "key": str,
            "type": InputType,
            "value": Any,
            "is_user_input": bool,
            "validator: Validator,
            "allowed_values": Dict,
            "required": bool,
        }
        """
        self.label = 'Input Label'  # type: str

        self.key = 'input_key'  # type: str

        self.type = InputType.Text  # type: InputType

        self.value = None  # type: Optional[Any]

        self.is_user_input = False  # type: bool

        self.validator = None  # type: Optional[Validator]

        self.allowed_values = None  # type: Optional[Dict]

        self.required = False  # type: bool

        if 'key' in options:
            self.key = str(options['key'])

            self.label = str(options['key']).capitalize()

        if 'label' in options:
            self.label = str(options['label'])

        if 'type' in options:
            if not isinstance(options['type'], InputType):
                raise ValueError("The value of the parameter 'type' must belong to the InputType enumeration.")

            self.type = options['type']

            if 'validator' not in options:
                self.validator = InputType.get_default_validator(self.type)

        if 'allowed_values' in options:
            self.allowed_values = options['allowed_values']

        if 'validator' in options:
            if not isinstance(options['validator'], Validator):
                raise TypeError("Parameter 'validator' must implement the Validator interface.")

            self.validator = options['validator']

        if 'is_user_input' in options:
            self.is_user_input = bool(options['is_user_input'])

        if 'value' in options:
            self.value = options['value']

            if not self.is_valid():
                raise ValueError("Value informed is invalid.")

    def get_label(self):
        return self.label

    def is_valid(self, value=None):
        # type: (Optional[Any]) -> bool
        if value is None:
            if self.value is None:
                return not self.required

            value = self.value

        if self.allowed_values is not None:
            return value in list(self.allowed_values.values())

        if self.validator is None:
            return True

        return self.validator.is_valid(value)

    def values_are_loose(self):
        if self.allowed_values is None:
            return True

        return False

    def values_are_fixed(self):
        if self.allowed_values is not None:
            return True

        return False

    def get_fixed_value(self):
        if isinstance(self.value, Enum):
            return self.value.value

        if self.value is not None:
            try:
                return self.allowed_values[self.value]
            except KeyError:
                return self.allowed_values[int(self.value)]

        return None

    def set_value_from_gui(self, value):
        if self.values_are_fixed():
            self.value = self.allowed_values.keys()[self.allowed_values.values().index(value)]
        else:
            self.value = value

    def __str__(self):
        try:
            return ','.join(map(str, self.value))
        except TypeError:
            return str(self.value)


class InputGroup:
    label = 'Group Label'  # type: str

    key = 'group_key'  # type: str

    inputs = {}  # type: Dict[str, Union[Input, 'InputGroup']]

    def __init__(self, options):
        """
        options = Dict {
            "label": str,
            "key": str,
            "inputs": Dict[str, Union[Input, InputGroup]],
        }
        """
        if 'label' in options:
            self.label = options['label']

        if 'key' in options:
            self.key = options['key']

        if 'inputs' in options:
            self.set_inputs(options['inputs'])

    def set_inputs(self, inputs):
        # type: (Dict[str, Union[Input, 'InputGroup']]) -> None
        self.inputs = {}

        for i in inputs:
            if isinstance(i, Input) or isinstance(i, InputGroup):
                self.inputs[i.key] = i
            else:
                raise TypeError("Input groups can only contain either other input groups, or inputs")

    def get_label(self):
        return self.label

    def has_user_input(self):
        for key in self.inputs:
            cur_input = self.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                return True

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                return True

        return False

    def is_valid(self):
        for key in self.inputs:
            if not self.inputs[key].is_valid():
                return False

        return True

    def __getitem__(self, item):
        element = self.inputs[item]

        if isinstance(element, Input):
            return element.value

        return element

    def __setitem__(self, key, value):
        if isinstance(value, Input) or isinstance(value, InputGroup):
            self.inputs[key] = value
        else:
            element = self.inputs[key]

            if isinstance(element, Input):
                element.value = value
            elif value is dict:
                for k in value:
                    element.inputs[k] = value[k]
            else:
                raise ValueError("When setting values for a InputGroup you must pass a dict as argument.")

    def copy_with_only_user_inputs(self):
        # type: () -> InputGroup
        input_group_copy = InputGroup({'label': self.label, 'key': self.key})

        input_group_copy.inputs = {}

        for i in self.inputs:
            if isinstance(self.inputs[i], Input):
                if self.inputs[i].is_user_input:
                    input_group_copy.inputs[i] = copy.deepcopy(self.inputs[i])

            if isinstance(self.inputs[i], InputGroup):
                if self.inputs[i].has_user_input():
                    input_group_copy.inputs[i] = self.inputs[i].copy_with_only_user_inputs()

        return input_group_copy

    def set_values_from_group(self, input_group):
        # type: ('InputGroup') -> None
        for i in input_group.inputs:
            from_input = input_group.inputs[i]

            cur_input = self.inputs[i]

            if isinstance(from_input, Input) and isinstance(cur_input, Input):
                cur_input.value = from_input.value

            if isinstance(from_input, InputGroup) and isinstance(cur_input, InputGroup):
                cur_input.set_values_from_group(from_input)
