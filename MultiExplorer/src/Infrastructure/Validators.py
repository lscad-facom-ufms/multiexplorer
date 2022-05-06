import re
from abc import ABCMeta, abstractmethod


class Validator:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'is_valid') and
                callable(subclass.is_valid))

    @abstractmethod
    def is_valid(self): raise NotImplementedError


class TextValidator:
    min_len = None

    max_len = None

    pattern = None

    def __init__(self, rules):
        if 'min_len' in rules:
            self.min_length = rules['min_length']

        if 'max_len' in rules:
            self.max_length = rules['max_length']

        if 'regexp' in rules:
            self.pattern = re.compile(rules['min_length'])

    def is_valid(self, value):
        if self.min_len is not None:
            if len(value) < self.min_len:
                return False

        if self.max_len is not None:
            if len(value) > self.max_len:
                return False

        if self.pattern is not None:
            if not self.pattern.match(value):
                return False

        return True


class IntegerValidator:
    min_val = None

    max_val = None

    def __init__(self, rules):
        if 'min_val' in rules:
            self.min_val = int(rules['min_val'])

        if 'max_val' in rules:
            self.max_val = int(rules['max_val'])

    def is_valid(self, value):
        try:
            value = int(value)
        except ValueError:
            return False

        if self.min_val is not None:
            if value < self.min_val:
                return False

        if self.max_val is not None:
            if value > self.max_val:
                return False

        return True


class FloatValidator:
    min_val = None

    max_val = None

    def __init__(self, rules):
        if 'min_val' in rules:
            self.min_val = float(rules['min_val'])

        if 'max_val' in rules:
            self.max_val = float(rules['max_val'])

    def is_valid(self, value):
        try:
            value = float(value)
        except ValueError:
            return False

        if self.min_val is not None:
            if value < self.min_val:
                return False

        if self.max_val is not None:
            if value > self.max_val:
                return False

        return True
