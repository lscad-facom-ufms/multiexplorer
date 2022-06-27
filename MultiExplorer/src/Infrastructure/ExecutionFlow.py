import threading
from abc import abstractmethod
import copy

from MultiExplorer.src.Infrastructure.Events import EventFirer, Event
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup


class Step(EventFirer):
    """
    This is the class used to extend MultiExplorer execution flows with new steps.
    
    Step classes should be implemented as SINGLETONS.

    The execution is handled in a separated execution thread, as to not cause the GUI to be stalled.
    """

    def __init__(self):
        super(Step, self).__init__()

        self.events = {
            Event.STEP_EXECUTION_STARTED: [],
            Event.STEP_EXECUTION_ENDED: [],
            Event.STEP_EXECUTION_FAILED: [],
        }

        self.execution_thread = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_label) and
                hasattr(subclass, 'execute') and
                callable(subclass.execute))

    """
    You should implement this method as static, returning the desired label for the Step.
    """
    @staticmethod
    def get_label():
        raise NotImplementedError

    """
        You should implement this method as static, returning True if the Step allows for user input.
    """
    @staticmethod
    def has_user_input(): return False

    def get_user_inputs(self):
        return {}

    def start_execution(self):
        self.execution_thread = threading.Thread(target=self.__execute__)

        self.execution_thread.start()

        self.fire(Event.STEP_EXECUTION_STARTED)

    def is_finished(self):
        if self.execution_thread is None:
            raise RuntimeError("Cannot check execution thread: thread not set.")

        if not self.execution_thread.is_alive():
            self.__finish__()

            return True

        return False

    """
    This method is not supposed to be evoked out of the "start_execution" method.
    
    You should implement in this method the handling of the execution of this step.
    
    You may throw any additional events or perform additional setup required before execution.
    """
    @abstractmethod
    def __execute__(self):
        raise NotImplementedError

    """
        This method is not supposed to be evoked out of the "is_finished" method.

        You should implement in this method the handling of the execution results of this step.

        In this method you should verify if the execution was successful, firing the appropriate events to notify
        other objects.
    """
    def __finish__(self):
        self.fire(Event.STEP_EXECUTION_ENDED)


class Adapter(object):
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


class ExecutionFlow(EventFirer):
    """
    This is the interface used to extend MultiExplorer with a new execution flow.

    ExecutionFlow classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        super(ExecutionFlow, self).__init__()

        self.steps = {}

        self.cur_step = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title))

    @staticmethod
    def get_label(self): raise NotImplementedError

    def get_steps(self): return self.steps

    def get_next_step(self):
        self.cur_step += 1

        try:
            return self.steps[self.cur_step]
        except IndexError:
            return None

    def execute(self):
        self.cur_step = -1

        self.execute_next_step()

    def execute_next_step(self):
        next_step = self.get_next_step()

        if next_step is not None:
            next_step.add_handler(Event.STEP_EXECUTION_ENDED, self.execute_next_step)

            next_step.start_execution()
        else:
            self.finish()

    def finish(self): pass
