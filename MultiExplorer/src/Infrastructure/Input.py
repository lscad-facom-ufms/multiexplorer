from enum import Enum
from abc import ABCMeta, abstractmethod


class InputType(Enum):
    input = 0
    group = 1
    text = 2


class Validator(metaclass=ABCMeta):
    """
    This is the interface used to extend MultiExplorer with a new execution flow.

    Validator classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'is_valid') and
                callable(subclass.is_valid))

    @abstractmethod
    def is_valid(self): raise NotImplementedError


class Input:
    label = 'Label'

    type = InputType.input

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
