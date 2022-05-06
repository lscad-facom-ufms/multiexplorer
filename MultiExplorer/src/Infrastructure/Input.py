from enum import Enum


class InputType(Enum):
    Input = 0
    Text = 1


class Input:
    label = 'Label'

    type = InputType.Input

    value = None

    validator = None

    def __init__(self, options):
        if 'label' in options:
            self.label = options['label']

        if 'type' in options:
            self.type = options['type']

        if 'validator' in options:
            self.type = options['type']

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

    def get_label(self):
        return self.label

    def is_valid(self):
        for input_in_the_group in self.inputs:
            if not input_in_the_group.is_valid():
                return False

        return True
