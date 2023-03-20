import copy

from abc import abstractmethod
from threading import Thread
from typing import List, Optional, Dict, Union
from MultiExplorer.src.Infrastructure.Events import EventFirer, Event
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup
from MultiExplorer.src.config import PATH_RUNDIR


class Step(EventFirer):
    """
    This is the class used to extend MultiExplorer execution flows with new steps.

    The execution is handled in a separated execution thread, as to not cause the GUI to be stalled.
    """

    def __init__(self):
        super(Step, self).__init__()

        self.output_path = None  # type: Optional[str]

        self.adapter = None  # type: Optional[Adapter]

        self.presenter = None  # type: Optional[Presenter]

        self.events = {
            Event.STEP_EXECUTION_STARTED: [],
            Event.STEP_EXECUTION_ENDED: [],
            Event.STEP_EXECUTION_FAILED: [],
        }

        self.execution_thread = None  # type: Optional[Thread]

        self.execution_exception = None  # type: Optional[BaseException]

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
    def has_user_input():
        return False

    def set_output_path(self, abs_path):
        self.output_path = abs_path

        if self.adapter is not None:
            self.adapter.set_output_path(abs_path)

    def get_user_inputs(self):
        return {}

    def copy_input_values(self, inputs):
        # type: (List[Input]) -> None
        if self.adapter is not None:
            self.adapter.copy_input_values(inputs)
        else:
            raise NotImplementedError("Since this Step uses no Adapter it must implement it's own input copy.")

    def start_execution(self):
        self.execution_thread = Thread(target=self.__execute__)

        self.fire(Event.STEP_EXECUTION_STARTED)

        self.execution_thread.start()

    def is_finished(self):
        if self.execution_thread is None:
            raise RuntimeError("Cannot check execution thread: execution thread not set.")

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

    """
    Should return a dictionary with all presentable results.
    """

    def get_results(self):
        # type: () -> Dict
        raise NotImplementedError

    def get_presenter(self):
        return self.presenter


class Adapter(object):
    """
        This is the class used to extend MultiExplorer execution flows with new external tools.

        Adapter classes are mainly responsible to dealing with the inputs and outputs of the external tools they handle.
        """

    def __init__(self):
        self.output_path = None  # type: Optional[str]

        self.inputs = {}  # type: Dict[str, Union[Input, InputGroup]]

        self.stashed_user_inputs = None  # type: Optional[Dict[str, Union[Input, InputGroup]]]

    def set_inputs(self, inputs):
        # type: (List[Union[Input, InputGroup]]) -> None
        for i in inputs:
            if isinstance(i, Input) or isinstance(i, InputGroup):
                self.inputs[i.key] = i
            else:
                raise TypeError("Argument 'inputs' must be an array composed solely of objects that belongs either to "
                                "the Input or the InputGroup classes.")

    def get_user_inputs(self):
        # type: () -> Dict[str, Union[Input, InputGroup]]
        user_inputs = {}

        for key in self.inputs:
            cur_input = self.inputs[key]

            if isinstance(cur_input, Input) and cur_input.is_user_input:
                user_inputs[key] = cur_input

            if isinstance(cur_input, InputGroup) and cur_input.has_user_input():
                user_inputs[key] = cur_input

        return user_inputs

    def copy_user_inputs(self):
        # type: () -> Dict[str, Union[Input, InputGroup]]
        copied_user_inputs = {}

        for key in self.inputs:
            if isinstance(self.inputs[key], Input) and self.inputs[key].is_user_input:
                copied_user_inputs[key] = copy.deepcopy(self.inputs[key])

            if isinstance(self.inputs[key], InputGroup) and self.inputs[key].has_user_input():
                copied_user_inputs[key] = self.inputs[key].copy_with_only_user_inputs()

        return copied_user_inputs

    def stash_user_inputs(self):
        self.stashed_user_inputs = self.copy_user_inputs()

    def pop_user_inputs(self):
        if self.stashed_user_inputs is not None:
            self.copy_input_values(self.stashed_user_inputs)

            self.stashed_user_inputs = None

    def copy_input_values(self, inputs):
        for key in inputs:
            if isinstance(inputs[key], Input) and isinstance(self.inputs[key], Input):
                self.inputs[key].value = inputs[key].value

            if isinstance(inputs[key], InputGroup) and isinstance(self.inputs[key], InputGroup):
                self.inputs[key].set_values_from_group(inputs[key])

    def set_output_path(self, abs_path):
        self.output_path = abs_path

    def get_output_path(self):
        if self.output_path is None:
            return PATH_RUNDIR

        return self.output_path


class ExecutionFlow(EventFirer):
    """
    This is the interface used to extend MultiExplorer with a new execution flow.
    """

    def __init__(self):
        super(ExecutionFlow, self).__init__()

        self.steps = []  # type: List[Step]

        self.cur_step = -1  # type: int

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title))

    @staticmethod
    def get_label():
        raise NotImplementedError

    @staticmethod
    def get_info():
        raise NotImplementedError

    def get_output_path(self):
        raise NotImplementedError

    def get_steps(self):
        # type: () -> List[Step]
        return self.steps

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

            next_step.add_handler(Event.STEP_EXECUTION_FAILED, self.handle_step_failure)

            next_step.start_execution()
        else:
            self.finish()

    """
    Handling step failure is optional.
    
    By default, execution will halt.
    """

    def handle_step_failure(self, step):
        self.finish()

    def finish(self):
        pass

    """
    Returns a dict with all the presentable results
    """

    def get_results(self):
        # type: () -> Dict
        raise NotImplementedError

    """
    Returns a list with all the result presenters
    """
    def get_presenters(self):
        # type: () -> List
        raise NotImplementedError
