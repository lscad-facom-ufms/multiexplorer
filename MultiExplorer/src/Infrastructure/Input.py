import collections

from enum import Enum

from MultiExplorer.src.Infrastructure.Validators import Validator


class InputType(Enum):
    Input = 0
    Text = 1
    Integer = 2
    Float = 3

    @staticmethod
    def belongs(value):
        return value in range(0,3)


class Input:
    label = 'Label'

    key = 'key'

    type = InputType.Input

    value = None

    validator = None

    def __init__(self, options):
        if 'key' in options:
            self.key = str(options['key'])

            self.label = str(options['key']).capitalize()

        if 'label' in options:
            self.label = str(options['label'])

        if 'type' in options:
            if not InputType.belongs(int(options['type'])):
                raise ValueError("Parameter 'type' must belong to the InputType enumeration.")

            self.type = int(options['type'])

        if 'validator' in options:
            if not isinstance(options['validator'], Validator):
                raise TypeError("Parameter 'validator' must implement the Validator interface.")

            self.type = options['validator']


    def get_label(self):
        return self.label

    def is_valid(self):
        if self.validator is None:
            return True

        return self.validator.is_valid(self.value)


class InputGroup:
    label = 'Group Label'

    inputs = []

    def __init__(self, options):
        if 'label' in options:
            self.label = options['label']

        if 'inputs' in options:
            self.inputs = options['inputs']

    def get_label(self):
        return self.label

    def is_valid(self):
        for input_in_the_group in self.inputs:
            if not input_in_the_group.is_valid():
                return False

        return True
