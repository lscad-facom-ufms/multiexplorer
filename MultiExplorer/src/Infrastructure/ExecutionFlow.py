from abc import ABCMeta, abstractmethod
import copy

from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup


class Step:
    __metaclass__ = ABCMeta
    """
    This is the class used to extend MultiExplorer execution flows with new steps.
    
    Step classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title) and
                hasattr(subclass, 'has_user_input') and
                callable(subclass.has_user_input))

    @abstractmethod
    def get_label(self): raise NotImplementedError

    @abstractmethod
    def has_user_input(self): raise NotImplementedError


class Adapter:
    """
        This is the class used to extend MultiExplorer execution flows with new external tools.

        Adapter classes are mainly responsible to dealing with the inputs and outputs of the external tools they handle.
        """
    def __init__(self):
        self.inputs = {}

    def set_inputs(self, inputs):
        for i in inputs:
            if isinstance(i, Input) or isinstance(i, InputGroup):
                self.inputs[i.key] = i
            else:
                raise TypeError("Argument 'inputs' must be an array composed solely of objects that belongs either to "
                                "the Input or the InputGroup classes.")

    def get_user_inputs(self):
        user_inputs = {}

        for key in self.inputs:
            cur_input = self.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                user_inputs[key] = cur_input

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                user_inputs[key] = cur_input

        return user_inputs

    def copy_user_inputs(self):
        copied_user_inputs = {}

        for key in self.inputs:
            cur_input = self.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                copied_user_inputs[key] = copy.deepcopy(cur_input)

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                copied_user_inputs[key] = cur_input.copy_with_only_user_inputs()

        return copied_user_inputs


class ExecutionFlow:
    __metaclass__ = ABCMeta
    """
    This is the interface used to extend MultiExplorer with a new execution flow.

    ExecutionFlow classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title) and
                hasattr(subclass, 'get_steps') and
                callable(subclass.get_steps))

    @abstractmethod
    def get_label(self): raise NotImplementedError

    @abstractmethod
    def get_steps(self): raise NotImplementedError
